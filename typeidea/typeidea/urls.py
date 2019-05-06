"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.sitemaps import views as sitemap_views

from .custom_site import custom_site
from blog.views import (
    IndexView, CategoryView, TagView,
     PostView, AuthorView, SearchView
)
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from config.views import LinkListView
from comment.views import CommentView


urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('admin/', custom_site.urls),    #以上admin.site是自带的一个site，而custom_site是我们自定义的site

    url(r'^$', IndexView.as_view(), name='all_posts'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^author/(?P<author_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^post_detail/(?P<post_id>\d+).html$', PostView.as_view(), name='post_detail'),

    url(r'^links/$', LinkListView.as_view(), name='links'),

    url(r'^comment/$', CommentView.as_view(), name='comment'),

    url(r'^rss/$', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}, name='sitemap'),
]
