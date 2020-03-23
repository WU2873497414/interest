from django.template import Library
from app01 import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


register = Library()

@register.inclusion_tag('left_menu.html')
def my_menu(username):
    user_obj = models.Userinfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 提供侧边栏所需要的所有的数据
    # 1.查询当前用户每一个分类及分类下的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(num=Count('article')).values_list('name','num','pk')
    # 2.查询当前用户每一个标签级标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(num=Count('article')).values_list('name','num','pk')
    # 3.按照年月分组
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(num=Count('pk')).values_list('month','num')
    return locals()