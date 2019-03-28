from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def news_01(request):
    posts = Post.objects.all()
    post_lists = list()
    for count, post in enumerate(posts):
        post_lists.append("No.{}: ".format(str(count)) + str(post) + "<hr>")
        post_lists.append("<small>" + str(post.body) + "</small><br><br>")
    return HttpResponse(post_lists)
