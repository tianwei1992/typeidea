# Create your models here.
from  __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Post(models.Model):
    STATUS_ITEMS = (
        (1, '上线'),
        (2, '草稿'),
        (3, '删除'),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    desc = models.CharField(max_length=255, blank=True, verbose_name="摘要")
    category = models.ForeignKey('Category', verbose_name="分类", on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', verbose_name="标签", related_name='post_set')

    content = models.TextField(verbose_name="内容", help_text="注：目前仅支持Markdown格式数据")
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "文章"
    
    def __str__(self):
        return self.title
    
    @staticmethod
    def get_by_tag(tag_id):
        """如果对应tag存在，只展示该tag下关联的文章; 否则，没有文章可展示"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
            tag = None
        else:
            post_list = tag.post_set.select_related('owner', 'category').filter(status=1)    # select_related()把Post对应Foreign Key提前查出，缓存备用，在模板渲染时直接用，避免N+1问题，提升性能

        return post_list, tag
        
    @staticmethod
    def get_by_category(category_id):
        """如果对应category存在，只展示该category下关联的文章; 否则，展示所有的文章"""
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            post_list = Post.objects.filter(status=1)
            category = None
        else:
            post_list = Post.objects.select_related('owner', 'category').filter(Q(category__id=category_id) & Q(status=1))
        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=1)
        return queryset

class TestManager(models.Manager):
    def get_queryset(self):
        return super(TestManager, self).get_queryset().filter(status=1)

class Category(models.Model):
    objects = TestManager()

    STATUS_ITEMS = (
        (1, '可用'),
        (2, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")

    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=1)

        nav_cates = []
        normal_cates = []

        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                normal_cates.append(cate)
        return {
            'navs': nav_cates,
            'normals': normal_cates,
        }

class Tag(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")

    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'
    
    def __str__(self):
        return self.name

