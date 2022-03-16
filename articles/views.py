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
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'articles/articles.html', {'posts': posts})


def post_detail(request, pk):
    if request.method == "POST":
        if request.POST['post_delete'] is not None:
            return redirect('post_delete', pk=pk)

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


def show_category(request, cat_id):
    posts = Post.objects.filter(published_date__lte=timezone.now()).filter(cat=cat_id).order_by('-published_date')
    return render(request, 'articles/article_category.html', {'posts': posts, 'cat_id': cat_id})


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')
