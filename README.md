# django-orcid

> 🍣 Use https://docs.allauth.org/en/latest/socialaccount/providers/orcid.html instead.

A Django App handling ORCID.org OAuth Authentication. Extends the Django User model and overrides frontent login.

## Installation

Copy the folder 'django_orcid' to your project directory and add the following to your ```INSTALLED APPS``` statement.

```python
INSTALLED_APPS = [
    ...
    'django_orcid',
    ...
]
```

You also need to add the authentication backend to the ```AUTHENTICATION_BACKENDS``` like so:

```python
AUTHENTICATION_BACKENDS = [
    'django_orcid.backends.OrcidBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

Lastly you need to run ```manage.py makemigrations``` to generate all necessary migrations depending on your database.

## Configuration

All necessary configuration is handled in ```settings.py```. After optaining an ORCID.org API key and secret, and after registering your redirect URI with ORCID, you can enter them here.

```python
# Authorization Url with ORCID
ORCID_AUTHORIZATION_URL = "https://sandbox.orcid.org/oauth/authorize"
# The requested scope
REQUESTED_SCOPE = "/read-limited" # If multiple scopes are desired, separate them with whitespaces
## Your Apps Client ID with ORCID
ORCID_CLIENT_ID = "" # Your Client ID from ORCID.org members API
## Your Apps secret wird ORCID
ORCID_CLIENT_SECRET = "" # Client Secret provided by ORCID.org members API
## Your Authentication langing page, as registered with ORCID
REDIRECT_URI = "<your base url>/accounts/auth" # redirect URI as registered with ORCID.org
## URL of ORCID-API to be used
ORCID_URL = "https://api.sandbox.orcid.org/v3.0/" # members API to be used
## URL for ORCID OAuth authentication
ORCID_OAUTH_URL = 'https://sandbox.orcid.org/oauth/token' # OAuth Authentication URL to be used
FROM_EMAIL = '' # The email adress from where your users shall receive notifications
IP_ADDRESS_HEADER = 'X-Forward-For' # The header where a user's IP Adress is stored. Default config for NGINX reverse proxy
```

As default ORCID's sandbox API is configured in. In Addition to your ORCID credentials you need an email adress, from which your users will be notified about a login from a new location. To achieve this, django-orcid does need to know from wich IP-Adress the login-attempt originated from. Since it's possible to use django-orcid in an app behind a reverse proxy, you may need to change the header where the client's IP-Address is stored.

You can request multiple scopes in ```REQUESTED_SCOPE``` by simply seperating them with white-spaces.

## Templates
Django-Orcid ships will all necessary templates. Though it expects to find a ```base.html``` template to extend and it also expects *Bootstrap 5* and its Javascript to be present in ```STATICROOTjs/bootstrap.bundle.min.js```. Please include *Bootstrap 5* into ```static/account.scss``` to render the templates properly. 
Django-Orcid uses SCSS, so please have your Django configured to use [Django-Compressor](https://github.com/django-compressor/django-compressor).

## Dependencies
Django-Orcid is pretty self contained, but does need some dependencies nonetheless.

- [Django-Compressor](https://github.com/django-compressor/django-compressor) To facilitate SCSS rendering. This can easily be changed by reverting to regular css
- [Django-Cryptography](https://pypi.org/project/django-cryptography/) To protect userdata, such as access tokens, refresh tokens and personal data.
- [Python Requests](https://pypi.org/project/requests/) To facilitate communication with ORCID's servers

## Tested on

- Python 3.9
- Wagtail 2.14
- Django 3.2
