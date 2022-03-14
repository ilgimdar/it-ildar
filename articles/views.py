from django.core.files.storage import FileSystemStorage
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
            selected_category = request.POST['cat']
            cat = Category.objects.get(name=selected_category)
            post = form.save(commit=False)
            post.cat = cat
            post.photo = request.FILES['post_image']
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            print("NOT VALID")
    else:
        form = PostForm()
    cats = Category.objects.all()
    return render(request, 'articles/post_new.html', {'form': form, 'cats': cats})


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


def show_category(request, cat_id):
    posts = Post.objects.filter(published_date__lte=timezone.now()).filter(cat=cat_id).order_by('published_date')
    cats = Category.objects.all()

    return render(request, 'articles/article_category.html', {'posts': posts, 'cats': cats, 'cat_id': cat_id})
