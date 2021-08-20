from datetime import datetime, timedelta

import jwt

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import validators


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True,
        db_index=True,
    )
    first_name = models.CharField(
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters only.'),
        validators=[validators.validate_field]
    )
    last_name = models.CharField(
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters only.'),
        validators=[validators.validate_field]
    )
    status = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.username = f'{self.first_name}{self.last_name}'
        super().save(*args, **kwargs)

    @property
    def token(self):
        """ Get token """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """ Generate web token JSON """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'
        ordering = ['-date_joined']

