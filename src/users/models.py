from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import validators


class User(AbstractUser):
    """
    Model users.
    """
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
    subscribers = models.ManyToManyField(
        'self',
        related_name='user_subscribers',
        blank=True,
        symmetrical=False
    )
    subscribed_on_users = models.ManyToManyField(
        'self', related_name='subscribed',
        blank=True,
        symmetrical=False
    )

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.username = f'{self.first_name}{self.last_name}'
        super().save(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'
        ordering = ['-date_joined']

