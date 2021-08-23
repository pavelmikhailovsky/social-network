from django.contrib import admin

from .models import Groups, Post


@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
