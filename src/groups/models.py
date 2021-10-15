from django.conf import settings
from django.db import models


class Groups(models.Model):
    """
    Model groups.
    """
    name = models.CharField(max_length=200, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image-group/', blank=True)
    description = models.TextField(max_length=10000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner', null=True)
    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='administrators',)
    redactors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='redactors',
    )
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_subscribers')
    category = models.CharField(max_length=150)  # in future or model or choices field

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'


class Post(models.Model):
    """
    Model posts.
    """
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    image = models.ImageField(upload_to='image-post/', blank=True, null=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    like = models.OneToOneField('Like', on_delete=models.CASCADE, related_name='post_like')

    def __str__(self):
        return f'{self.create_at} -- {self.group.name}'

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Like(models.Model):
    """
    Model likes.
    """
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users')

    class Meta:
        db_table = 'like'
        verbose_name = 'like'
        verbose_name_plural = 'likes'


