from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    #當檔案透過管理者後台http://127.0.0.1:8000/admin上傳時, media/post_files資料夾會被自動建立。
    #blank=True 可不上傳檔案; 
    post_files = models.FileField(upload_to='post_files/', blank=True) 

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
