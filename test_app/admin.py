from django.contrib import admin

from .models import Article, UserResponse, User

admin.site.register(Article)
admin.site.register(UserResponse)
admin.site.register(User)
