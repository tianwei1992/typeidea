from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from .models import Post, Tag, Category


def post_list(request, tag_id=None, category_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_tag(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,    # tag和category本身也是需要展示的，如果存在的话
        'tag': tag, 
        'post_list': post_list, 
    }

    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    context={
        'post':post,
    }

    return render(request, 'blog/detail.html', context=context)
