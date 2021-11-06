from django.contrib import admin
from django.contrib.admin.sites import site
from .models import Recipe, Comment, Like, DisLike
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(DisLike)
