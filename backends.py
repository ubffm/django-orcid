# authentication backends go here
# documentation: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#specifying-authentication-backends

import requests
import random
import orcidaccount.settings as settings
import json
from django.core.mail import send_mail
from datetime import datetime
from hashlib import sha3_256

from http import HTTPStatus
from django.contrib.auth.backends import BaseBackend

from django.contrib.auth.models import User

from orcidaccount.models import OrcidUser


class OrcidBackend(BaseBackend):

    def create_login_hash(self, request, user) -> str:

        if user.orciduser.salt == '':
            user.orciduser.salt = str('%0x' % random.randrange(16**30))
            user.orciduser.save()

        to_encode = user.orciduser.salt[:13] + request.headers.get(settings.IP_ADDRESS_HEADER) + user.orciduser.salt[13:]
        return sha3_256(to_encode.encode('utf-8')).hexdigest()

    def check_last_login(self, request, user) -> bool:

        current_login = self.create_login_hash(request, user)

        if current_login != user.orciduser.last_login:
            return False
        else:
            return True

    def login_notification_email(self, request, user):
        from_email = settings.FROM_EMAIL
        subject = f'Login attempt on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
        to_email = user.email

        message = f"""
            Hello,

            There was a login attempt on {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}.
            Somebody just logged onto our service with your ORCID credentials.

            Details:
            Time of login: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            IP-Adress: {request.headers.get(settings.IP_ADDRESS_HEADER)}
            Browser and Operating System: {request.headers.get('user-agent')}

            If that was not you, please change your password on ORCID and contact us.

            If it was you, please ignore this email.
            Please do not reply to this email.

            Have a nice day.
        """

        send_mail(subject, message, from_email, [to_email], fail_silently=True)

    def orcid_oauth_request(self, token):
        headers = {'Accept': 'application/json'}
        post_data = {
            "client_id": settings.ORCID_CLIENT_ID,
            "client_secret":settings.ORCID_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": token,
            "redirect_uri": settings.REDIRECT_URI
        }

        response = requests.post(settings.ORCID_OAUTH_URL, headers=headers, data=post_data)

        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise Exception('Something went wrong during communication with orcid. Please close this window and try again later.')

    def orcid_profile_request(self, orcid, token):
        headers = {'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
        url = f'{settings.ORCID_URL}{orcid}/record'

        return requests.get(url,headers=headers).json()

    def orcid_email_request(self, orcid, token):
        headers = {'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
        url = f'{settings.ORCID_URL}{orcid}/email'

        return requests.get(url,headers=headers).json()

    def authenticate(self, request, token=None):
        '''
            Get token from login page,
            Verify token with ORCID
            Get userdata from ORCID
            See if USER is in database
                if yes: return USER
                if no: create user with userdata and return USER
            if verification fails:
                return NONE

            Example: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#writing-an-authentication-backend
        '''

        if token is None:
            return None

        userdata = self.orcid_oauth_request(token)

        if userdata.get('error') is None and userdata.get('orcid') is not None:
            # Authenticate or create a user
            try:
                user = User.objects.get(username=userdata.get('orcid'))

                # update user data data if necessary
                profile = self.orcid_profile_request(userdata.get('orcid'),userdata.get('access_token'))
                # get primary email:
                primary_mail = ''

                emails = self.orcid_email_request(userdata.get('orcid'), userdata.get('access_token'))

                if emails.get('email') is not None:
                    for email in emails.get('email'):
                        if email.get('email') is not None and email.get('primary') is True:
                            primary_mail = email.get('email')

                if user.first_name != profile.get('person').get('name').get('given-names').get('value'):
                    user.first_name = profile.get('person').get('name').get('given-names').get('value')
                if user.last_name != profile.get('person').get('name').get('family-name').get('value'):
                    user.last_name = profile.get('person').get('name').get('family-name').get('value')
                if user.email != primary_mail:
                    user.email = primary_mail

                user.orciduser.access_token = userdata.get('access_token')
                user.orciduser.token_type = userdata.get('token_type')
                user.orciduser.refresh_token = userdata.get('refresh_token')
                user.orciduser.expires_in = userdata.get('expires_in')
                user.orciduser.scope = userdata.get('scope')
                user.orciduser.profile = json.dumps(profile)

                user.save()
                user.orciduser.save()
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password, so an unusable password is set.
                # TODO: populate profile with additional information from ORCID.
                profile = self.orcid_profile_request(userdata.get('orcid'),userdata.get('access_token'))
                # get primary email:
                primary_mail = ''

                emails = self.orcid_email_request(userdata.get('orcid'), userdata.get('access_token'))

                if emails.get('email') is not None:
                    for email in emails.get('email'):
                        if email.get('email') is not None and email.get('primary') is True:
                            primary_mail = email.get('email')

                user = User(username=userdata.get('orcid'), first_name=profile.get('person').get('name').get('given-names').get('value'), last_name=profile.get('person').get('name').get('family-name').get('value'), email=primary_mail)
                user.is_staff = False
                user.is_superuser = False
                user.set_unusable_password()
                orcid_user = OrcidUser(user=user,access_token=userdata.get('access_token'),token_type=userdata.get('token_type'),refresh_token=userdata.get('refresh_token'),expires_in=userdata.get('expires_in'), scope=userdata.get('scope'))
                orcid_user.profile = json.dumps(profile)
                user.save()
                orcid_user.save()

            if self.check_last_login(request, user) is False:
                if user.email != '':
                    self.login_notification_email(request, user)
                user.orciduser.last_login = self.create_login_hash(request, user)
                user.orciduser.save()

            return user
        else:
            # Raise Access denied here
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
