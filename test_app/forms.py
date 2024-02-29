from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.conf import settings
from django.core.mail import send_mail
from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput
from .models import Article


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
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
                'category': TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'}),
                'media': ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'файл'}),
            }

        def form_valid(self, form):
            article = form.save(commit=False)
            article.author = self.request.user
            article.save()
            return super().form_valid(form)
