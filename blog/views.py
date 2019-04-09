from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    user = User.objects.first()

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})


def get_other_posts(post=None):
    # List every other posts and tell if it's already related or not
    related_posts = []

    if post:
        all_posts = Post.objects.exclude(pk=post.pk).all()
        already_related = post.related_posts.all()
    else:
        all_posts = Post.objects.all()
        already_related = []

    for other_post in all_posts:
        related_posts.append((other_post, other_post in already_related))

    return related_posts

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    other_posts=get_other_posts()
    return render(request, 'blog/post_edit.html', {'form': form, 'posts': get_other_posts()})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post, 'posts': get_other_posts(post)})
