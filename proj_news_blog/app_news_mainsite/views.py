from django.shortcuts import render, redirect
from .models import Post
from datetime import datetime
from django.core.files.storage import FileSystemStorage

def news_01(request):
    posts = Post.objects.all()
    now = datetime.now()
    return render(request, 'index.html', locals())

def showpost_news_01(request, slug):
    #now = datetime.now()
    try:
        post = Post.objects.get(slug = slug)
        if post != None:
            return render(request, 'post.html', locals())
    except:
        return redirect('news_01/')

def html_for_upload(request): #檔案會直接傳到media資料夾內，沒有另建其他資料夾
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['doc_upload_to_media']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'html_for_upload.html', context)
