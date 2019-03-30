from django.contrib import admin
from .models import Post

# 自訂Post顯示方式之類別
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','pub_date','post_files','photo')

admin.site.register(Post, PostAdmin)
