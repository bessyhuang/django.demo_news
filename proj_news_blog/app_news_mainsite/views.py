from django.shortcuts import render, redirect
from .models import Post
from datetime import datetime

def news_01(request):
    posts = Post.objects.all()
    now = datetime.now()
    post_lists = list()
    return render(request, 'index.html', locals())

def showpost_news_01(request, slug):
    #now = datetime.now()
    try:
        post = Post.objects.get(slug = slug)
        if post != None:
            return render(request, 'post.html', locals())
    except:
        return redirect('news_01/')
