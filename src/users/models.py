from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # TODO using validator for username field for examination validate data with regex, example Pavel Mikhailovsky -> OK
    status = models.CharField(max_length=500, blank=True, null=True)
    avatar_image = models.ImageField(upload_to='users/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='users/', blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'
