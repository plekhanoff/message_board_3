from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import request, HttpResponseRedirect
from django.http import Http404

from .forms import ArticleForm, CommonSignupForm, CommentForm, CommentDeleteForm

from .models import Article, Comment, User


@permission_required('polls.add_choice')
@login_required
def my_view(request):
    # Your view logic here
    return render(request, 'default.html')


def logout_view(request):
    logout(request)
    return redirect('index')


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
                return render(self.request, 'registration/invalid_code.html')
        return redirect('signup')


class SignupView(CreateView):
    form = CommonSignupForm
    model = User
    success_url = 'login'
    template_name = 'registration/signup.html'
    fields = ['username', 'email']


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'test_app/profile.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(author=self.request.user)
        context['articles'] = articles
        return context


class ArticleList(ListView):
    model = Article
    template_name = 'test_app/index.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter()
        context['articles'] = articles
        return context


class ArticleView(View):
    model = Article
    form_class = ArticleForm
    template_name = 'test_app/article_read.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'

    def get(self, request, pk):
        try:
            article = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404("Статья не найдена")

        context = {
            self.context_object_name: article,
        }
        return render(request, self.template_name, context)


class ArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('test_app.article_create',)
    raise_exception = True
    model = Article
    form_class = ArticleForm
    template_name = 'test_app/article_create.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_save(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        form.save()
        return redirect('profile', self.object.pk)


class ArticleDetail(LoginRequiredMixin, DetailView):
    permission_required = ('test_app.article_create',)
    model = Article
    template_name = 'test_app/article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_id'] = self.kwargs.get('pk')
        return context


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('test_app.article_update',)
    model = Article
    form_class = ArticleForm
    template_name = 'test_app/article_update.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_save(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        form.save()
        return redirect('article_detail', self.object.pk)


class CommentCreate(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'test_app/comment_create.html'
    form_class = CommentForm
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.commentUser = self.request.user
        form.instance.commentArticle = Article.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def form_save(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        form.save()
        comment_user_email = form.instance.commentArticle.author.email
        send_email(to_email=comment_user_email, subject='Ваш коммент прочитали', message='Ваш коммент прочитали.')
        return redirect('article_read', self.object.pk)


def send_email(to_email, subject, message):
    email = EmailMessage(subject, message, to=[to_email])
    email.send()


class CommentUpdate(LoginRequiredMixin,UpdateView):
    permission_required = ('test_app.comment_edit',)
    model = Comment
    form_class = CommentForm
    template_name = 'test_app/comment_edit.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Comment, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_id'] = self.kwargs.get('pk')
        return context


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'test_app/delete.html'
    success_url = reverse_lazy('profile')


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentDeleteForm
    template_name = 'test_app/comment_delete.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
