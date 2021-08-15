from django.contrib.auth.models import AbstractUser
from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


class User(AbstractUser):
    # TODO using validator for username field for examination validate data with regex, example Pavel Mikhailovsky -> OK
    status = models.CharField(max_length=500, blank=True, null=True)
    image = models.ManyToManyField('UserImage', related_name='user_image_field', blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'


class UserImage(models.Model):
    avatar = VersatileImageField('Avatar', upload_to='user-image/', ppoi_field='image_ppoi')
    image_ppoi = PPOIField()

    def __str__(self):
        return f'{self.__class__.__name__}'
