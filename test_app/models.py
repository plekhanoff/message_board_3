
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    pass


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = id
        self.id = id

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


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey('Article', on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=False)


class Comment(models.Model):
    objects = None
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    commentArticle = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='комментарий')
    text = models.TextField(verbose_name='коммент')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='время создания')
    status = models.BooleanField(default=False, verbose_name='статус')

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.commentArticle_id = None

    def __str__(self):
        return f'{self.commentUser} : {self.text} [:20] + ...'

    def get_absolute_url(self):
        return reverse('article_detail',kwargs={'pk' : self.commentArticle_id })

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарий'
        ordering = ['id']
