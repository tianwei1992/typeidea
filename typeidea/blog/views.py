from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import Post, Tag, Category
from config.models import SideBar


class CommonMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class BasePostsView(CommonMixin, ListView):     # ListView自带Paginator，需要同步在html中引入分页符号
    queryset = Post.latest_posts()    #这里可以指定model=Post，之后会自动让queryset设置为所有posts，于是这里指定queryset要指定的结果
    template_name = 'blog/list.html'
    context_object_name = 'post_list'
    paginate_by = 3


class IndexView(BasePostsView):
    pass


class CategoryView(BasePostsView):
    def get_queryset(self):
        """在基础queryset的基础上要按Category多进行一次过滤"""
        qs = super(CategoryView, self).get_queryset()
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cate_id)
        return qs
    
    def get_context_data(self, **kwargs):
        """在基础context的基础上要增加一个category对象"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context


class TagView(BasePostsView):
    def get_queryset(self):
        """在基础queryset的基础上要按Tag多进行一次过滤"""
        qs = super(TagView, self).get_queryset()
        tag_id = self.kwargs.get('tag_id')
        qs = qs.filter(tags__id=tag_id)    #注意因为tags是多对多的键，这里是2个下划线
        return qs
    def get_context_data(self, **kwargs):
        """在基础context的基础上要增加一个Tag对象"""
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context


class PostView(CommonMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id' #这是从url接受的名字吗？
