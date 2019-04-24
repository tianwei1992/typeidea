## version 0.1.0 -- 2019-04-17

init project

## Finish Chatper 5 & 6 -- 2019-04-20

    完成了Model和Admin。Model是一切的基础，Admin就是管理Model在页面上的呈现。
1.  Model字段还有IntegerField带choices属性，null设定数据库层面允许为空，blank设定业务层面。
2.  QuerySet是核心对象：懒加载和链式调用；Django还封装了F表达式、Q表达式、Count、Sum来支持聚合。
3.  Admin做的比较多，最简单可以继承admin.ModelAdmin然后通过注册与某个Model绑定，如果想要个性化可以定制list_fields, fields, fieldsets等等特性，还可以重载save_model()和get_query()方法，在每次保存时自动用request.user填充onwner名字。其中fields的元素既可以是Model原有的字段，也可以由具有某种处理过程的自定义字段, 比如def operator(self, obj)以及def post_count(self, obj)。这些字段本质上是方法。
4.  对Admin的定制分成3类，定制这个字段怎么显示，比如定制form特性(自定义class ModelForm然后将实例赋值给form字段)；定制字段的内容，比如定制fileter特性；定制字段显示的布局和位置，fieldset特定，inline特性。
5.  不同url路由到不同site分配不同内容：创建AdminSite实例，然后分配内容。

## Finish Chatper 7 -- 2019-04-24
    
    完成了View，从视图函数到基于类的视图。逻辑很简单，基础代码很容易，主要做了很多抽取：Model中可以集中定义View的内容如get_latest()，也可以集中Template中的内容如content_html()，在其他位置直观调用。
1. 对于Post模型来说，tags是多对多字段，category是一对多字段，处理上有点区别。
2. 在Post Model中，get_latest(cls)被定义为classmethod，get_by_tag(tag_id)是staticmethod。（区别是在于意义？latest属于类，get_xxx属于实例？）
3. 比较好的一点是把context(dict)提出来写，方便后续用context.update({})扩展。
4. 查询默认只带出对象的正常字段（外键、多对多键因为是对象，不缓存），用select_related()将指定字段一起带出，避免第2次查询，提升性能 。
    ```Post.objects.select_related('owner', 'category')```
5. 对于有choices=STATUS_ITEMS的字段，消除选项中的魔法数字，换成名字有意义的常量。
6. 模板中除了常规{{ sidebar.html }}，还可以有更加个性化的自定义的{{ sidebar.content_html }}, 按照不同的sidebar类型给予不同的展示风格。
7. 最后升级到基于类的视图，用了mixin。最顶层的是CommonMixin，ListView和DetailView。其中CommenMixin重写了get_context_data()方法，把侧边栏和导航栏一起加入到context中，这也是所有页面都要用到的，所以是common类型。在下面的一层，CommonMixin和ListView一混合，指定queryset = Post.latest_posts只要最新文章而不是全部集合，就成为BasePostsView; CommonMixin和DetailView一混合，指定DetailView空缺的pk_url_kwarg = 'post_id'就成为PostView，文章详情页。再往下一层， CategoryView和TagView都是从BasePostsView派生而来，因为要按Tag/Category过滤数据，所以重写了get_queryset；因为context里面要新加入当前的Tag/Category展示，所以重写了get_context_data()。

    OK!
