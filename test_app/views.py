from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import request

from .forms import ArticleForm, CommonSignupForm, CommentForm

from .models import Article, Comment, UserResponse


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


class SignupView(CreateView):
    form = CommonSignupForm
    model = User
    success_url = '/registration/login'
    template_name = 'registration/signup.html'
    fields = ['username', 'email']


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(author=self.request.user)
        context['articles'] = articles
        return context


class ArticleList(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'article'
    paginate_by = 9


class ArticleCreate(CreateView):
    permission_required = ('test_app.article_detail',)
    raise_exception = True
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_save(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        form.save()
        return redirect('article_detail', self.object.pk)


class ArticleDetail(DetailView):
    permission_required = ('test_app.article_create',)
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_id'] = self.kwargs.get('pk')
        return context


class ArticleUpdate(UpdateView):
    permission_required = ('test_app.article_update',)
    model = Article
    form_class = ArticleForm
    template_name = 'article_update.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'article_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commentUser = self.request.user
        comment.commentArticle_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_id'] = self.kwargs['pk']
        return context

    def comment_article(request, article_id, author=None):
        article = get_object_or_404(Article, pk=article_id)
        comment = Comment(user=request.user, article=article, text=request.POST['text'])
        comment.save()
        request.send_email(author.email, 'Новый коментарий на объявление',
                   'У вас новый комментарий на объявление "{}"'.format(article.title))
        request.send_email(request.user.email, 'комментарий отослан',
                   'ваш комментарий на объявление "{}" отправлен автору.'.format(article.title))
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
        request.send_email(comment.user.email, 'ваш отклик прочтён',
                   'Автор объявления "{}" Прочёл ваш комментарий.'.format(comment.article.title))
        return redirect('article_detail', pk=comment.article.id)

    def send_email(to_email, subject, message):
        email = EmailMessage(subject, message, to=[to_email])
        email.send()


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('index')


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'delete.html'
    success_url = reverse_lazy('index')
