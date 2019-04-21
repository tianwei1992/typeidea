from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from .models import Post, Tag, Category


def post_list(request, tag_id=None, category_id=None):
    tag = None
    category = None

    if tag_id:
        """如果对应tag存在，只展示该tag下关联的文章; 否则，没有文章可展示"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = Post.objects.filter(Q(tag__id=tag_id) and Q(status=1))
    elif category_id:
        """如果对应tag存在，只展示该tag下关联的文章; 否则，展示所有的文章"""
        try:
            category = Category.objects.get(id=category_id)
            post_list = Post.objects.filter(Q(category__id=category_id) and Q(status=1))
        except Category.DoesNotExist:
            post_list = Post.objects.filter(status=1)
    else:
            post_list = Post.objects.filter(status=1)

    context = {
        'category': category,    # tag和category本身也是需要展示的，如果存在的话
        'tag': tag, 
        'post_list': post_list, 
    }

    return render(request, 'blog/list.html', context=context)
