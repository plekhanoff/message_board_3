from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .forms import ArticleForm, CommonSignupForm
from .models import Article, Comment


@permission_required('polls.add_choice')
@login_required
def my_view(request):
    # Your view logic here
    return render(request, 'default.html')


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'invalid_code.html')
        return redirect('signup')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(author=self.request.user)
        context['articles'] = articles
        return context


class SignupView(CreateView):
    form = CommonSignupForm
    model = User
    success_url = '/registration/login'
    template_name = 'registration/signup.html'
    fields = ['username', 'email']


@login_required
def comment_article(request, article_id, author=None):
    article = get_object_or_404(Article, pk=article_id)
    comment = Comment(user=request.user, article=article, text=request.POST['text'])
    comment.save()
    send_email(author.email, 'New comment on the article', 'You have a new comment on the article "{}"'.format(article.title))
    send_email(request.user.email, 'Your comment has been sent', 'Your comment on the article "{}" has been sent to the author.'.format(article.title))
    return redirect('article_detail', pk=article_id)


def get_comments(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment.objects.filter(article=article)
    return render(request, 'article_detail.html', {'article': article, 'comments': comments})


@login_required
def read_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.read = True
    comment.save()
    send_email(comment.user.email, 'Your review has been read', 'The author of the article "{}" has read your comment.'.format(comment.article.title))
    return redirect('article_detail', pk=comment.article.id)


def send_email(to_email, subject, message):
    email = EmailMessage(subject, message, to=[to_email])
    email.send()


class ArticleList(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'article'
    paginate_by = 9


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('index')


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'delete.html'
    success_url = reverse_lazy('index')
