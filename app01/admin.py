from django.contrib import admin
from app01 import models
# Register your models here.

class BookConfig(admin.ModelAdmin):
    list_display = ['username','password','register_time','avatar']
    list_display_links = ['password']
    search_fields = ['username','password']
    list_filter = ['blog']

    def patch_init(self,request,queryset):
        print(queryset)  # <QuerySet [<Userinfo: tank>, <Userinfo: admin>, <Userinfo: oscar>, <Userinfo: jason>, <Userinfo: egon>]>

    patch_init.short_description = '批量更新'
    actions = [patch_init]


admin.site.register(models.Userinfo,BookConfig)
admin.site.register(models.Blog)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.UpAndDown)
admin.site.register(models.Comment)