from django.shortcuts import render, redirect
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash, authenticate
)

logger = logging.getLogger(__name__)


# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        if request.GET.get('next') is not None:
            return redirect(request.GET.get('next'))
        elif request.GET.get('next') is None:
            return redirect('profile')


def auth(request):
    token = request.GET.get('code')
    user = authenticate(request, token=token)
    if user is not None:
        auth_login(request, user)
        # Render to a success page.
        return render(request, 'auth.html')
    else:
        # Return an 'invalid login' error message.
        return render(request, 'auth_failed.html')


@login_required
def profile(request):
    context = {}

    return render(request, 'profile.html', context)


@login_required
def delete_account(request):

    # If the page is called by itself, display a form to delete an account.
    if request.method == 'GET':
        # return template
        return render(request, 'delete_account.html')
    elif request.method == 'POST':
        orcid = request.POST.get('orcid')
        user = User.objects.get(username=orcid)

        if user == request.user:
            user.delete()
            auth_logout(request)
        else:
            logger.error('attempted account deletion')

    return render(request, 'account_deleted.html')
