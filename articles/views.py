from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from blog.models import Category

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    cats = Category.objects.all()
    return render(request, 'articles/articles.html', {'posts': posts, 'cats': cats})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'articles/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'articles/post_new.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    title = Post.objects.get(pk=pk).title
    text = Post.objects.get(pk=pk).text
    return render(request, 'articles/post_edit.html', {'title': title, 'text': text})


def show_category(request, pk):
    posts = Post.objects.filter(published_date__lte=timezone.now()).filter(cat=pk).order_by('published_date')
    cats = Category.objects.all()

    return render(request, 'articles/articles.html', {'posts': posts, 'cats': cats})