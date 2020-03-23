from django.shortcuts import render,HttpResponse,redirect,reverse
from app01 import myform
from app01 import models
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Min,Count,Sum,Avg
from django.db.models.functions import TruncMonth
# Create your views here.
def register(request):
    form_obj = myform.MyRegForm()
    if request.method == 'POST':
        back_dic = {'code':1000,'msg':''}
        # 对用户提交的数据先进行校验 forms
        form_obj = myform.MyRegForm(request.POST)  # username password confirm_password email
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data  # {四个键值对}
            clean_data.pop('confirm_password')  # {username    password    email}
            file_obj = request.FILES.get('avatar')
            if file_obj:  # 一定要判断用户是否上传了文件
                clean_data['avatar'] = file_obj  # {username  password email   avatar}
            models.Userinfo.objects.create_user(**clean_data)
            back_dic['msg'] = '注册成功'
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request,'register.html',locals())


def login(request):
    if request.method == "POST":
        back_dic = {'code':1000,'msg':''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 1.先校验验证码是否正确  忽略大写小
        if request.session.get('code').upper() == code.upper():
            # 2.在校验用户名和密码是否正确
            user_obj = auth.authenticate(request,username=username,password=password)
            if user_obj:
                # 3.保存用户登录状态
                auth.login(request,user_obj)  # 就可以在任意位置通过request.user获取到当前登录对象 并且 request.user.is_authenticated()判断当前用户是否登录
                back_dic['msg'] = '登录成功'
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
    return render(request,'login.html')


from PIL import Image,ImageDraw,ImageFont
import random
from io import BytesIO,StringIO
"""
内存管理器模块
BytesIO  保存数据 并且在获取的时候 是以二进制的方式给你
StringIO  保存数据 并且在获取的时候 是以字符串的方式给你
"""
"""
Image       生成图片
ImageDraw   在图片上写字
ImageFont   控制字的字体样式
"""
def get_random():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)



# 图片验证码相关
def get_code(request):
    # 推导步骤1:直接发送后端存在的图片
    # with open(r'avatar/444.jpg','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 推导步骤2:利用pillow模块自动生成图片  pip3 install pillow
    # img_obj = Image.new('RGB',(360,35),get_random())  # 图片对象生成完毕
    # # 你得利用文件操作先保存起来
    # with open(r'xxx.png','wb') as f:
    #     img_obj.save(f,'png')
    # # 然后再利用文件操作将图片数据读取并发送
    # with open(r'xxx.png','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 推导步骤3:临时存储数据并且能够随时取出的地方
    # img_obj = Image.new('RGB',(360,35),get_random())
    # # 先生成一个io对象
    # io_obj = BytesIO()  # 你就将对象看成是文件句柄即可
    # # 存储数据
    # img_obj.save(io_obj,'png')
    # # 读取数据
    # return HttpResponse(io_obj.getvalue())  # 获取二进制的数据
    # 推导步骤4(最终推导)  在图片上写字
    img_obj = Image.new('RGB',(360,35),get_random())
    # 将生成好的图片对象交给ImageDraw
    img_draw = ImageDraw.Draw(img_obj)  # 生成了一个画笔对象
    # 字体样式
    img_font = ImageFont.truetype('static/font/111.ttf',30)

    # 随机验证码    大小写英文加数字   五位 每一位都可以是大写字母或小写字母或数字
    code = ''
    for i in range(5):
        upper_str = chr(random.randint(65,90))
        lower_str = chr(random.randint(97,122))
        random_int = str(random.randint(0,9))
        # 随机选取一个
        tmp = random.choice([upper_str,lower_str,random_int])
        # 朝图片上写一个
        img_draw.text((i*60+60,0),tmp,get_random(),img_font)
        # 存储写的字
        code += tmp
    print(code)
    # 这个验证码后面其他视图函数可能要用到  找个地方存储一下 并且这个地方全局的视图函数都能访问
    request.session['code'] = code
    io_obj = BytesIO()
    img_obj.save(io_obj,'png')
    return HttpResponse(io_obj.getvalue())



def home(request):
    # 查询当前网站所有的文章 展示到前端页面上
    article_queryset = models.Article.objects.all()
    return render(request,'home.html',locals())

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


@login_required
def set_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # 1 先判断旧密码是否正确
        is_right = request.user.check_password(old_password)
        if is_right:
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                return redirect(reverse('login'))
            else:
                return HttpResponse('两次密码不一致')
        else:
            return HttpResponse("原密码错误")
            # 2 新旧密码不一致
            # if not old_password == new_password:
            #     # 3 判断新密码不能为空
            #     if not len(new_password) == 0:
            #         # 4 两次密码
            #         if new_password == confirm_password:
            #             request.user.set_password(new_password)
            #             request.user.save()
            #             return redirect(reverse('login'))



def site(request,username,**kwargs):
    user_obj = models.Userinfo.objects.filter(username=username).first()

    if not user_obj:  # 404页面
        return render(request,'error.html')
    blog = user_obj.blog
    # 有当前用户所有的文章
    article_list = models.Article.objects.filter(blog=blog)
    """
    侧边栏筛选功能到底是晒什么
    晒的是当前这个用户下面的所有的文章 再进行晒选
    本质其实就是对已经查询出来的article_list再进行晒选操作
    """
    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'category':
            # 按照分类晒选
            article_list = article_list.filter(category_id=param)
        elif condition == 'tag':
            # 按照标签晒选
            article_list = article_list.filter(tags__id=param)
        else:
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year,create_time__month=month)
    # # 1.查询当前用户每一个分类及分类下的文章数
    # category_list = models.Category.objects.filter(blog=blog).annotate(num=Count('article')).values_list('name','num','pk')
    #
    #
    # # 2.查询当前用户每一个标签级标签下的文章数
    # tag_list = models.Tag.objects.filter(blog=blog).annotate(num=Count('article')).values_list('name','num','pk')
    #
    #
    # # 3.按照年月分组
    # date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(num=Count('pk')).values_list('month','num')
    return render(request,'site.html',locals())




def article_detail(request,username,article_id):
    # 将文章查询出来
    article_obj = models.Article.objects.filter(pk=article_id).first()
    blog = article_obj.blog
    # 还应该获取当前文章所有的评论信息
    comment_list = models.Comment.objects.filter(article=article_obj)
    if not article_obj:
        return render(request,'error.html')
    return render(request,'article_detail.html',locals())

import json
from django.db.models import F
from django.utils.safestring import mark_safe
def updown(request):
    if request.is_ajax():
        if request.method == 'POST':
            back_dic = {'code':1000,'msg':''}
            is_up = request.POST.get('is_up')  # 是一个字符串格式的json数据
            article_id = request.POST.get('article_id')
            is_up = json.loads(is_up)  # 将json格式的字符串数据转成python对应的数据类型
            # print(is_up,type(is_up))
            """
            点赞点踩业务逻辑
                1.判断当前用户是否登录
                2.当前这篇文章是否是当前用户自己写的
                3.当前这篇文章用户是否已经点过
                4.操作数据库 完成数据修改
                    1.点赞点踩添加数据的时候
                    2.文章表里面对应的普通字段也得修改
            """
            # 1.判断当前用户是否登录
            if request.user.is_authenticated():
                # 2.当前这篇文章是否是当前用户自己写的
                article_obj = models.Article.objects.filter(pk=article_id).first()
                if not article_obj.blog.userinfo == request.user:
                    # 3.当前这篇文章用户是否已经点过
                    is_click = models.UpAndDown.objects.filter(user=request.user,article=article_obj).exists()
                    if not is_click:
                        # 操作数据库 完成数据修改
                        if is_up:
                            models.Article.objects.filter(pk=article_id).update(up_num = F('up_num') + 1)
                            back_dic['msg'] = '点赞成功'
                        else:
                            models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                            back_dic['msg'] = '点踩成功'
                        models.UpAndDown.objects.create(user=request.user,article=article_obj,is_up=is_up)
                    else:
                        back_dic['code'] = 2000
                        back_dic['msg'] = '你已经点过了不能在点了'
                else:
                    back_dic['code'] = 3000
                    back_dic['msg'] = '你个臭不要脸的 不能给自己点'

            else:
                back_dic['code'] = 4000
                back_dic['msg'] = mark_safe('请先<a href="/login/">登录</a>')
            return JsonResponse(back_dic)

from django.db import transaction

def comment(request):
    if request.is_ajax():
        if request.method == 'POST':
            back_dic = {'code':1000,'msg':''}
            article_id = request.POST.get('article_id')
            content = request.POST.get('content')
            # parent_id如果有值那么正常存储 如果没有值也无所谓就存空 也符合要求
            parent_id = request.POST.get('parent_id')
            with transaction.atomic():
                models.Comment.objects.create(user=request.user,article_id=article_id,content=content,parent_id=parent_id)
                models.Article.objects.filter(pk=article_id).update(comment_num = F('comment_num') + 1)
                back_dic['msg'] = '评论成功'
            return JsonResponse(back_dic)

from app01.utils.mypage import Pagination
@login_required
def backend(request):
    article_list = models.Article.objects.filter(blog=request.user.blog)
    page_obj = Pagination(current_page=request.GET.get('page',1),all_count=article_list.count())
    page_queryset = article_list[page_obj.start:page_obj.end]

    return render(request,'backend/backend.html',locals())

from bs4 import BeautifulSoup
@login_required
def add_article(request):
    tag_list = models.Tag.objects.filter(blog=request.user.blog)
    category_list = models.Category.objects.filter(blog=request.user.blog)
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags_list = request.POST.getlist('tags')
        category_id = request.POST.get('category')
        # 先生成一个模块对象
        soup = BeautifulSoup(content,'html.parser')
        # print(soup.text)  # 获取纯文本
        tags = soup.find_all()
        # print(tags)
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()  # 删除标签
        # 先简单的除暴的直接截取内容的150个字符串
        # desc = content[0:150]
        desc = soup.text[0:150]
        # 操作数据
        article_obj = models.Article.objects.create(title=title,content=str(soup),desc=desc,category_id=category_id,blog=request.user.blog)
        # 去文章与标签表的第三张关系报中手动录入数据   bulk_create
        obj_list = []
        for tag_id in tags_list:
            obj_list.append(models.Article2Tag(article=article_obj,tags_id=tag_id))
        models.Article2Tag.objects.bulk_create(obj_list)
        return redirect('/backend/')
    return render(request,'backend/add_article.html',locals())


import os
from BBS import settings
def upload_img(request):
    back_dic = {'error': 0}
    # 获取用户上传的图片 然后保存到本地
    if request.method == 'POST':

        # print(request.FILES)  打印键值对
        file_obj = request.FILES.get('imgFile')
        # 手动拼接文件存储的文件路径
        file_path = os.path.join(settings.BASE_DIR,'media','article_img')
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        # 文件操作
        # 手动拼接文件名全路径
        img_path = os.path.join(file_path,file_obj.name)
        with open(img_path,'wb') as f:
            for line in file_obj:
                f.write(line)
        _url = '/media/article_img/%s'%file_obj.name
        back_dic['url'] = _url
    """
    //成功时
{
        "error" : 0,
        "url" : "http://www.example.com/path/to/file.ext"
}
//失败时
{
        "error" : 1,
        "message" : "错误信息"
}
    
    
    """
    return JsonResponse(back_dic)


@login_required
def set_avatar(request):
    # 展示用户之前的头像
    # 再让用户上传一个新头像
    if request.method == 'POST':
        file_obj = request.FILES.get("avatar")
        # 1 不会自动拼接路径
        # models.Userinfo.objects.filter(pk=request.user.pk).update(avatar=file_obj)
        # 2 可以 了解
        request.user.avatar = file_obj
        request.user.save()
        return redirect('/home/')
    return render(request,'set_avatar.html',locals())