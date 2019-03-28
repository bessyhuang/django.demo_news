# django.demo_news
Django 最新消息

git clone https://github.com/bessyhuang/django.demo_news.git
cd django.demo_news/

## 1. 虛擬環境初始化

> sudo apt-get install -y python3-pip

> sudo pip3 install virtualenv

> virtualenv venv

> source venv/bin/activate

## 2. 安裝 Django

> (venv) ~/django.demo_news$ pip install django

* 查看安裝了哪些套件
  > pip freeze


* 把安裝的套件匯出成`requirements.txt`
  > pip freeze > requirements.txt


## 3. 建立project

> django-admin startproject proj_news_blog


## 4. 建立app

> cd proj_news_blog/

> python manage.py startapp app_news_mainsite

* 查看`proj_news_blog`整個專案的樹狀結構
  > cd ..

  > pip install tree

  > tree proj_news_blog

* 移除`tree`套件
  > pip uninstall tree

---
