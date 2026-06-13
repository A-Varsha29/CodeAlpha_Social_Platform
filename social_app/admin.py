from django.contrib import admin
from .models import Profile, Post, Comment, Follow

#Register your models here so they show up in the admin panel
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
