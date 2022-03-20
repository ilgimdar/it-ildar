from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView, FormView

from blog.models import Category
from blog.models import Post
from .forms import PostForm
from .utils import *


class PostList(DataMixin, ListView):
    model = Post
    template_name = 'articles/articles.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.order_by('-published_date')


class PostCat(DataMixin, ListView):
    paginate_by = 3
    paginate_orphans = 1
    model = Post
    template_name = 'articles/article_category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(cat=self.kwargs['cat_id']).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(cat_selected=self.kwargs['cat_id'])
        return dict(list(context.items()) + list(c_def.items()))


class PostDetail(View):
    template_name = 'articles/post_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            if request.POST['post_delete'] is not None:
                return redirect('post_delete', pk=self.kwargs['pk'])
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return render(request, self.template_name, {'post': post})


class PostNew(FormView):
    form_class = PostForm
    template_name = 'articles/post_new.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            selected_category = request.POST['cat']
            cat = Category.objects.get(name=selected_category)
            post = form.save(commit=False)
            post.cat = cat
            if request.FILES and request.FILES['post_image'] is not None:
                post.photo = request.FILES['post_image']
            else:
                post.photo = 'default.png'
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            print("NOT VALID")
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, self.template_name, {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            selected_category = request.POST['cat']
            cat = Category.objects.get(name=selected_category)
            post.cat = cat
            if request.FILES and request.FILES['post_image'] is not None:
                post.photo = request.FILES['post_image']
            post.save()
            return redirect('post_detail', pk=post.pk)
    post_obj = Post.objects.get(pk=pk)
    title = post_obj.title
    text = post_obj.text
    photo = post_obj.photo
    cat = post_obj.cat
    context = {
        'title': title,
        'text': text,
        'photo': photo,
        'cat': cat
    }
    return render(request, 'articles/post_edit.html', context=context)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')


def login(request):
    return HttpResponse('login')
