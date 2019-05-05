from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import Post, Tag, Category
from config.models import SideBar
from comment.forms import CommentForm
from comment.models import Comment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path),
        })
        return context

    def get(self, request, *args, **kwargs):
        """加入访问统计"""
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        """pv和uv都放在cache中，由pv_key和uv_key为key，获取值。
            如果当前已存在，说明上一次还未过期，认为是同一次，不做处理，否则+1.
            默认cache是内存缓存，只适用于单进程"""
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path) 
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效, 不重复+1

        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效，不重复+1

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)



class AuthorView(BasePostsView):
    # 和完整文章列表页相比，就是增加了过滤
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('author_id')
        return queryset.filter(owner_id=author_id)


class SearchView(BasePostsView):
    # 和完整文章列表页相比，增加了过滤，展示的context_data还多了一项keywords
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
