
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Email должен быть установлен')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    code = models.CharField(max_length=8, blank=True, null=True)
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    username = models.CharField(verbose_name='Имя пользователя', max_length=30, unique=True)
    objects = CustomUserManager()


class Article(models.Model):
    objects = None
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'дд'),
        ('buyers', 'Торговцы'),
        ('gildmasters', 'Хозяева_гильдий'),
        ('quest', 'квест'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевики'),
        ('spellmasters', 'Хозяева_заклятий'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=88)
    text = models.TextField()
    category = models.CharField(max_length=16, choices=TYPE, default='Танки')
    media = models.FileField(upload_to='media/', default='default.png')

    def preview(self):
        preview = f'{self.text[0:123]} + "..."'
        return preview

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.author:
            self.author = self.author if self.author else self.request.user
        super().save(*args, **kwargs)


class Comment(models.Model):
    objects = True
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор комментария')
    commentArticle = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='комментарий к статье :')
    text = models.TextField(verbose_name='коммент')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='время создания')
    status = models.BooleanField(default=False, verbose_name='статус')

    def __str__(self):
        return f'{self.commentUser} : {self.text} [:20] + ...'

    def get_absolute_url(self):
        return reverse('article_read',kwargs={'pk': self.commentArticle_id})

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарий'
        ordering = ['id']
