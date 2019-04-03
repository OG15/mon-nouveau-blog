from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    user = User.objects.first()

    return render(request, 'blog/post_list.html', {'posts': posts})
