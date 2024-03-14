from django.contrib.auth.views import LoginView
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', ArticleList.as_view(), name='index'),
    path('<int:pk>/', ArticleUpdate.as_view(), name='article_update'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/updata', ArticleUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('<int:pk>/comment/create', CommentCreate.as_view(), name='comment_create'),
    path('article/detail/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
]
