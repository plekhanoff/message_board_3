from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', ArticleList.as_view(), name='index'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/article/update', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm', ConfirmUser.as_view(), name='confirm_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('<int:pk>/comment/create', CommentCreate.as_view(), name='comment_create'),
    path('article/detail/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('article/read/<int:pk>/', ArticleView.as_view(), name='article_read'),
    path('<int:pk>/edit', CommentUpdate.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),
    path('<int:pk>/response/', Response.as_view(), name='response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

