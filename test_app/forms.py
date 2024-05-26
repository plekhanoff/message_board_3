from allauth.account.forms import SignupForm

from django.conf import settings
from django.core.mail import send_mail
from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput, Select
from django import forms
from string import hexdigits

import random

from .models import Article, Comment


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код для активации',
            message=f'Код активации вашего аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'media']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Название объявления'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст объявления'}),
            'media': ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'изображение'}),
            'category': Select(attrs={'class': 'form-control', 'placeholder': 'категория'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Введите текст'}
        widgets = {'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 100, 'rows': 10})}


class ArticleDeleteForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'media']


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']