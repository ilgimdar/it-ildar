from django.shortcuts import render
from blog.models import Post
from django.utils import timezone
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'articles/articles.html', {'posts': posts})


def post_new(request):
    form = PostForm()
    return render(request, 'articles/post_edit.html', {'form': form})
