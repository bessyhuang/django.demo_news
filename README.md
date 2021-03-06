# django.demo_news
Django 最新消息
```
git clone https://github.com/bessyhuang/django.demo_news.git
cd django.demo_news/
```

## 1. 虛擬環境初始化

```
sudo apt-get install -y python3-pip
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

## 2. 安裝 Django

```
(venv) ~/django.demo_news$ pip install django
```

* 查看安裝了哪些套件
  > pip freeze
  
  Django==2.1.7
  
  pytz==2018.9

* 把安裝的套件匯出成`requirements.txt`
  > pip freeze > requirements.txt

## 3. 建立project

```
django-admin startproject proj_news_blog
```

## 4. 建立app

```
cd proj_news_blog/
python manage.py startapp app_news_mainsite
```

* 查看`proj_news_blog`整個專案的樹狀結構
  > cd ..

  > pip install tree

  > tree proj_news_blog

* 移除`tree`套件
  > pip uninstall tree


## 5. 執行Django

```
python manage.py runserver
```

---

## 6. 改成Mariadb

* 安裝文件：django mariadb ubuntu 18.04.odt
* Flask - 資料庫：https://hackmd.io/s/ryWzxlTL4#

---

## 7. 初始化 Django `settings.py` & 定義 最新消息的資料表 `models.py`

* pub_date 欄位, 以 timezone.now 的方式讓它自動產生, 需要 pytz 套件：

```
pip install pytz
```

* 建立資料庫和Django間的中介檔案：

```
python manage.py makemigrations
```

* 同步更新資料庫的內容：

```
python manage.py migrate
```

## 8. 啟用admin管理介面 & 註冊並自訂Post顯示方式之類別 `admin.py`

```
python manage.py createsuperuser

使用者名稱 (leave blank to use 'user'): admin
電子信箱: 
Password: admin
Password (again):admin
```

* 確認 `models.py` Post資料表內的欄位有寫入 db_demo 資料庫內

```
sudo mysql -u root -p

MariaDB [(none)]> SHOW DATABASES;
MariaDB [(none)]> USE db_demo;
MariaDB [db_demo]> show tables;
MariaDB [db_demo]> show columns from app_news_mainsite_post;

+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int(11)      | NO   | PRI | NULL    | auto_increment |
| title    | varchar(200) | NO   |     | NULL    |                |
| slug     | varchar(200) | NO   |     | NULL    |                |
| body     | longtext     | NO   |     | NULL    |                |
| pub_date | datetime(6)  | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
5 rows in set (0.002 sec)
```

---

## 9. 讀取資料庫中的內容 `view.py` `urls.py`

* `view.py`

```
from django.http import HttpResponse
from .models import Post
```

* `urls.py`

```
from django.urls import path, include
from app_news_mainsite.views import news_01
```

---

## 10. 建立網頁輸出模板template `index.html` & 設定`settings.py`的TEMPLATE區塊 & 調整`views.py`

* 建立`templates`＆ `static` 資料夾

```
(venv) ~/django.demo_news/proj_news_blog$ mkdir templates
(venv) ~/django.demo_news/proj_news_blog$ mkdir static

(venv) ~/django.demo_news/proj_news_blog$ cd ..
(venv) ~/django.demo_news$ tree proj_news_blog/

proj_news_blog/
├── app_news_mainsite
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-36.pyc
│   │       └── __init__.cpython-36.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   └── views.cpython-36.pyc
│   ├── tests.py
│   └── views.py
├── manage.py
├── proj_news_blog
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── settings.cpython-36.pyc
│   │   ├── urls.cpython-36.pyc
│   │   └── wsgi.cpython-36.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static
└── templates

8 directories, 23 files
```

* 設定`settings.py`的TEMPLATE區塊

```
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

* 調整`views.py` [把posts和now(現在時刻)丟到模板] , 並新增`index.html`

```
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from datetime import datetime

def news_01(request):
    posts = Post.objects.all()
    now = datetime.now()
    return render(request, 'index.html', locals())
```

---

## 11. 網址對應`urls.py` & 調整`views.py` `index.html` & 建立`post.html`

* `index.html`

```
{% for post in posts %}
	<h1><a href="/post/{{ post.slug }}">{{ post.title }}</a></h1>
{% endfor %}
```

* `urls.py`

```
from app_news_mainsite.views import showpost_news_01

urlpatterns = [
    path('post/<slug:slug>/', showpost_news_01),
]
```

* `views.py`

```
from django.shortcuts import redirect

def showpost_news_01(request, slug):
    try:
        post = Post.objects.get(slug = slug)
        if post != None:
            return render(request, 'post.html', locals())
    except:
        return redirect('news_01/')
```

* `post.html`

```
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Welcome to Latest News</title>
</head>
<body>
	<h1>{{ post.title }}</h1>
	<hr>
	<h3>{{ post.body }}</h3>
	<br>
	<p><a href="/news_01">back to HOME</a></p>
</body>
</html>
```

---

## 12. 共用模板的使用`base.html` `header.html` `footer.html`

* `base.html`

```
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>{% block title %} {% endblock %}</title>
</head>
<body>
	<div style="background-color: #FFECC9">
		{% include 'header.html' %}
	</div>

	{% block headmessage %} {% endblock %}
	{% block content %} {% endblock %}

	<div style="background-color: #FFECC9">
		{% include 'footer.html' %}
	</div>
</body>
</html>
```

---

## 13. JavaScript & CSS 檔案的引用 (Bootstrap) & 圖片的引入

* 將`bootstrap.min.css` & `bootstrap.min.js`放入`static`資料夾中

* (Bootstrap) `base.html`

```
{% load static %}

<link rel="stylesheet" href="{% static "css/bootstrap.min.css" %}">
<link href="{% static "js/bootstrap.min.js" %}">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
```

* `settings.py`

```
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

* 圖片的引入 (需要建立`static/images`資料夾)

```
{% load static %}
<img src="{% static "images/rabbit.png" %}" alt="" width="10%">
```

---

## 14. 更改排版 & `index.html`顯示摘要與自訂日期格式

* `index.html`顯示摘要與自訂日期格式

```
{% block content %}
<div class="card" style="width: 60rem;">
	<div class="card-header">一般事務</div>

	<ul class="list-group list-group-flush">
	{% for post in posts %}
	<li class="list-group-item">
		<a href="/post/{{ post.slug }}">{{ post.title }}</a>
		<p>{{ post.body | truncatechars:60 }}</p>
		<p>發布時間: {{ post.pub_date | date:"Y-m-d, h:m:s" }}</p>
	</li>
	{% endfor %}
	</ul>
</div>
{% endblock %}
```

---

## 15. 新聞文章的HTML內容處理 (Markdown)

* 安裝`Markdown`套件

```
pip install django-markdown-deux
```

* `settings.py`

```
INSTALLED_APPS = [
    'markdown_deux',
]
```

* `pip freeze > requirements.txt`

```
Django==2.1.7
django-markdown-deux==1.0.5
markdown2==2.3.7
PyMySQL==0.9.3
pytz==2018.9
```

* `post.html`

```
{% load markdown_deux_tags %}

<h3>Content:<br><br>{{ post.body | markdown}}</h3>
```

* 透過進入管理者後台`http://127.0.0.1:8000/admin`，直接`張貼圖片`於內文中。使用第三方圖形檔案服務網站（imgur.com）。

```
![test](http://8maple.ru/wp-content/uploads/2018/08/3561-01.jpg)

####《延禧攻略》（英語：Story of Yanxi Palace）是2018年古裝劇，由吳謹言及佘詩曼領銜主演，秦嵐及聶遠特別主演，並由許凱及譚卓聯合主演。
```

* `mystyle.css`自訂統一的圖片顯示大小

```
img[alt = "test" ] {
  width: 50%;
}
```

* `base.html`引入`mystyle.css`

```
<link rel="stylesheet" href="{% static "css/mystyle.css" %}">
```

---

## 16. Django網站的構成以及配合

* 移動`static` 、`templates` (彈性？須討論網站的構成)

  > 此作法的目的：讓模板和靜態檔案也跟著app跑

```
(venv) user@fengchia-swift-sf314-52:~/django.demo_news$ tree proj_news_blog/

proj_news_blog/
├── app_news_mainsite
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-36.pyc
│   │       └── __init__.cpython-36.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   └── views.cpython-36.pyc
│   ├── static
│   │   ├── css
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.css.map
│   │   │   ├── bootstrap-grid.css
│   │   │   ├── bootstrap-grid.css.map
│   │   │   ├── bootstrap-grid.min.css
│   │   │   ├── bootstrap-grid.min.css.map
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap.min.css.map
│   │   │   ├── bootstrap-reboot.css
│   │   │   ├── bootstrap-reboot.css.map
│   │   │   ├── bootstrap-reboot.min.css
│   │   │   ├── bootstrap-reboot.min.css.map
│   │   │   └── mystyle.css
│   │   ├── images
│   │   │   └── rabbit.png
│   │   └── js
│   │       ├── bootstrap.bundle.js
│   │       ├── bootstrap.bundle.js.map
│   │       ├── bootstrap.bundle.min.js
│   │       ├── bootstrap.bundle.min.js.map
│   │       ├── bootstrap.js
│   │       ├── bootstrap.js.map
│   │       ├── bootstrap.min.js
│   │       └── bootstrap.min.js.map
│   ├── templates
│   │   ├── base.html
│   │   ├── footer.html
│   │   ├── header.html
│   │   ├── index.html
│   │   └── post.html
│   ├── tests.py
│   └── views.py
├── manage.py
└── proj_news_blog
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-36.pyc
    │   ├── settings.cpython-36.pyc
    │   ├── urls.cpython-36.pyc
    │   └── wsgi.cpython-36.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

11 directories, 50 files
```

---

## 17. File Uploads (整合至`models.py`的`class Post`) & 修改`admin.py` `settings.py` `urls.py` `post.html`

* Django documentation: https://docs.djangoproject.com/en/2.1/
* File Uploads: https://docs.djangoproject.com/en/2.1/topics/http/file-uploads/
* NULL vs. BLANK: https://docs.djangoproject.com/en/dev/ref/models/fields/#null

```
### models.py ###
class Post(models.Model):
    post_files = models.FileField(upload_to='post_files/', blank=True)

### admin.py ###
# 自訂Post顯示方式之類別
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','pub_date','post_files')

### settings.py ###
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') #will build a file 'media' in same level path as manage.py

### urls.py ###
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

### post.html ###
{% if post.post_files %}
    <h3>post_files:</h3>
    <img src="{{ post.post_files.url }}" width="70%">
    {% else %}
    <p>No post_files ~</p>
{% endif %}
```

---

## 18. Image Uploads (整合至`models.py`的`class Post`) & 修改`admin.py` `post.html`

* 安裝`Pillow`套件

```
pip install Pillow
```

* `pip freeze > requirements.txt`

```
Django==2.1.7
django-markdown-deux==1.0.5
markdown2==2.3.7
Pillow==5.4.1
PyMySQL==0.9.3
pytz==2018.9
```

```
### models.py ###
class Post(models.Model):
    photo = models.ImageField(upload_to='photo/', blank=True)

### admin.py ###
# 自訂Post顯示方式之類別
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','pub_date','post_files','photo')

### post.html ###
{% if post.photo %}
<h3>photo:</h3>
<img src="{{ post.photo.url }}" width="70%">
{% else %}
<p>No photo ~</p>	
{% endif %}
```

---

## 19. Uploads (透過`html_for_upload.html`上傳檔案，檔案會直接傳到media資料夾內，沒有另建其他資料夾)

* `urls.py`

```
from app_news_mainsite.views import html_for_upload

urlpatterns = [
    path('html_for_upload/', html_for_upload, name='html_for_upload'), 
]
```

* `views.py`

```
from django.core.files.storage import FileSystemStorage

#檔案會直接傳到media資料夾內，沒有另建其他資料夾
def html_for_upload(request): 
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['doc_upload_to_media']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'html_for_upload.html', context)
```

* `html_for_upload.html`

```
{% extends 'base.html' %}

{% block title %}Upload File{% endblock %}

{% block content %} 
<div class="jumbotron">
<h1 class="display-4">Upload File</h1>
<p class="lead"></p>
<hr class="my-4">
<p></p>
<div class="form-group">
  	<form method="post" enctype="multipart/form-data" class="form-inline">
	  	<div class="form-group mx-sm-3 mb-2">
	  		{% csrf_token %}
		<input type="file" name="doc_upload_to_media" class="form-control-file">
		<button type="submit" class="btn btn-warning mb-2">Upload</button>
		</div>
	</form>
</div>

{% if url %}
<p>Uploaded File: <a href="{{ url }}">{{ url }}</a></p>
{% endif %}
</div>
{% endblock %}
```

