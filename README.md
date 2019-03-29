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


