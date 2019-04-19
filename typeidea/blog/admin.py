# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from typeidea.custom_site import custom_site

from .models import Post, Category, Tag
from .adminforms import PostAdminForm


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = _('分类过滤器')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        """
        返回所有可以作为过滤条件的选项
        """
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        """
        按每个过滤条件，返回结果集
        """
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
       'title', 'category', 'status',
       'owner', 'created_time', 'operator'
    ]# operator是自定义字段

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name', 'owner__username']
    
    # fields控制的是管理后台新增页面显示
    """
    fields = (
        ('title', 'category'),    # 元组表示，2个字段分布在1行
        'desc',
        'status',
        'content',
        'tags',
    )

    exclude = ('owner',)    # owner是自动填充，不在fields里面填写
    """

    actions_on_top = True

    save_on_bottom = True
    show_full_result_count = True

    filter_horizontal = ('tags', )    # 控制多选字段中，可选与选中的位置关系

    fieldsets = (  # 跟fields互斥, 分版块
        ('基础配置', {
            'fields': (('category', 'title'), 'desc', 'content')
        }),
        ('高级配置', {
            'fields': ('tags', 'status'),
        }),
    )
    
    def operator(self, obj):
        """一个自定义字段"""
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_site:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        """保存之前自动与当前user关联"""
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """通过重载，对list_display的结果进行过滤"""
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)


class PostInlineAdmin(admin.StackedInline):
    """在同一页面编辑关联数据"""
    fields = ('title', 'status')
    # extra = 2  # 控制额外多几个
    max_num = 4
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')
    inlines = [
        PostInlineAdmin,
    ]    # 在Category编辑页面，顺便一起展示Category关联的文章的编辑页面

    def save_model(self, request, obj, form, change):
        """保存之前自动与当前user关联"""
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def post_count(self, obj):
        """一个自定义字段"""
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display=('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        """保存之前自动与当前user关联"""
        obj.owner = request.user
        super().save_model(request, obj, form, change)
