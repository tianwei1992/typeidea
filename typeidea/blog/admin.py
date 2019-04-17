# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
       'title', 'category', 'status',
       'owner', 'created_time', 'operator'
    ]# operator是自定义字段

    list_filter = ['category']
    search_fields = ['title', 'category__name', 'owner__username']
    
    # fields控制的是管理后台新增页面显示
    fields = (
        ('title', 'category'),    # 元组表示，2个字段分布在1行
        'desc',
        'status',
        'content',
        'tags',
    )

    actions_on_top = True

    save_on_top = True
    show_full_result_count = True
    
    def operator(self, obj):
        """一个自定义字段"""
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        """保存之前自动与当前user关联"""
        obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        """保存之前自动与当前user关联"""
        obj.owner = request.user
        super().save_model(request, obj, form, change)

    def post_count(self, obj):
        """一个自定义字段"""
        return obj.post_set.count()
    post_count.short_description = '文章数量'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        """保存之前自动与当前user关联"""
        obj.owner = request.user
        super().save_model(request, obj, form, change)
