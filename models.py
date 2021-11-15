from django.db import models
from django.contrib.auth.models import User

from django_cryptography.fields import encrypt
# Create your models here.


class OrcidUser(models.Model):
    '''
        This is an extension for the standerd Django Usermodel to store and retrieve Data from ORCID.
    '''
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    access_token = encrypt(models.CharField(max_length=255))
    token_type = models.CharField(max_length=255)
    refresh_token = encrypt(models.CharField(max_length=255))
    expires_in = models.IntegerField()
    scope = models.CharField(max_length=255)
    salt = encrypt(models.CharField(max_length=50, default=''))
    last_login = models.CharField(max_length=256, default='')
    profile = encrypt(models.TextField(default=''))  # This field stores the entire user profile as Text. Needs to be parsed as JSON.
    # ORCID IS USERNAME!!!

    def __str__(self):
        return f'{self.user.username} ({self.user.last_name}, {self.user.first_name})'
