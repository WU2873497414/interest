"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from django.views.static import serve
from BBS import settings
# from django.shortcuts import HttpResponse
# def index1(request):
#     return HttpResponse('index')
# def index2(request):
#     return HttpResponse('index')




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 路由分发本质
    # url(r'^index/',([
    #         url(r'^index_1/',([
    #             url(r'^index_1_1/',([
    #
    #                                 ],None,None)),
    #             url(r'^index_1_2/',index2),
    #             url(r'^index_1_3/',index1),
    #                           ],None,None)),
    #         url(r'^index_2/',index2),
    #                 ],None,None)),

    # 注册功能
    url(r'^register/',views.register,name='register'),
    # 登录功能
    url(r'^login/',views.login,name='login'),

    # 图片验证码
    url(r'^get_code/',views.get_code,name='code'),

    # 首页搭建
    url(r'^home/',views.home,name='home'),

    # 退出登录
    url(r'^logout/',views.logout,name='logout'),

    # 修改密码
    url(r'^set_password/',views.set_password,name='set_pwd'),

    # 手动开设后端资源  将media文件夹下面所有的资源暴露给外界
    url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),

    # 谨慎使用
    # url(r'^app01/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT})

    # 点赞点踩业务逻辑
    url(r'^up_down/', views.updown),
    # 评论业务逻辑
    url(r'^comment/',views.comment),
    # 后台管理
    url(r'^backend/',views.backend),
    # 添加文章
    url(r'^add_article/',views.add_article),
    # 文章静态文件
    url(r'^upload_img/',views.upload_img),
    # 修改头像
    url(r'^set_avatar/',views.set_avatar),
    # 个人站点
    url(r'^(?P<username>\w+)/$',views.site,name='username'),

    # 个人站点侧边栏筛选功能
    # url(r'^(?P<username>\w+)/category/(?P<param>\d+)/',views.site),
    # url(r'^(?P<username>\w+)/tag/(?P<param>\d+)/',views.site),
    # url(r'^(?P<username>\w+)/archive/(?P<param>\w+)/',views.site),
    # 优化
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/',views.site),

    # 文章详情页
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/',views.article_detail),




]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns