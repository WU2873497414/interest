from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Userinfo(AbstractUser):
    phone = models.BigIntegerField(null=True,blank=True)  # blank告诉admin后台管理 该字段可以为空
    avatar = models.FileField(upload_to='avatar/',default='media/avatar/default.jpg')
    # 该字段你直接传文件即可 会自动将文件保存到avatar文件夹下  然后数据库里面存文件路径
    register_time = models.DateField(auto_now_add=True)
    blog = models.OneToOneField(to='Blog',null=True)


    class Meta:
        verbose_name_plural = '用户表'
        # verbose_name = '用户表'  # 自动加s后缀


    def __str__(self):
        return self.username

class Blog(models.Model):
    site_name = models.CharField(max_length=32)
    site_title = models.CharField(max_length=64)
    site_theme = models.CharField(max_length=64)
    # 该字段存的是用户自己写的css文件路径

    def __str__(self):  # 只能返回字符串数据类型
        return self.site_name


class Category(models.Model):
    name = models.CharField(max_length=32)

    blog = models.ForeignKey(to='Blog',null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog',null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=255)
    content = models.TextField()
    create_time = models.DateField(auto_now_add=True)

    # 数据库优化三个普通字段
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)

    # 外键字段
    category = models.ForeignKey(to='Category',null=True)
    blog = models.ForeignKey(to='Blog',null=True)
    tags = models.ManyToManyField(to='Tag',through='Article2Tag',through_fields=('article','tags'))


    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tags = models.ForeignKey(to='Tag')




class UpAndDown(models.Model):
    user = models.ForeignKey(to='Userinfo')
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField()


class Comment(models.Model):
    user = models.ForeignKey(to='Userinfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(max_length=255)
    create_time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(to='self',null=True)  # 语义更明确


