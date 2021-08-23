from django.db import models


class Groups(models.Model):
    """
    Model groups.
    """
    name = models.CharField(max_length=200, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='image-group/', blank=True)
    description = models.TextField(max_length=10000)
    # owner =
    # administrators =
    # redactors =
    # subscribers =
    category = models.CharField(max_length=150)  # in future or model or choices field

    def __str__(self):
        return self.name

    def get_number_subscribers(self): pass

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
    like = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.create_at} -- {self.group.name}'

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'









