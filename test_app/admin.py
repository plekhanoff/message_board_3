from django.contrib import admin

from .models import Article, User, Comment

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Comment)