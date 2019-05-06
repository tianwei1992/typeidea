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

## Finish Chatper 9 -- 2019-05-06

    基本完成博客主题。
1. 划分themes，比如bootstrap就是一套主题，里面包括templates和statics，其中statics又包括css和js。这些东西都是和前端密切关联的。
2. 新增2个页面，分别是按作者过滤，和按搜索结果过滤。直接继承完整版BasePostsView，然后重载get_queryset()和 get_context_data()实现过滤和新增展示字段。
3. 文章列表页、详情页、友链页不仅页面上有共同的机构，context_data也有固定共同的内容（侧边栏），所以统统继承自CommonMixin，而CommonMixin里面就唯一重载了get_context_data，把原来queryset指定的自动添加的Post以外的Sidebar也一起添加进去。   
4. 评论在两个页面都有，且页面的核心内容并不是comment而分别是Post和Link，于是为了复用，把评论区抽象成一个tag（comment_block），tag接收参数，通过传参的不同来不同的呈现。tag放在名为templatestags的文件夹下，本质上还是一个方法，只不过被tag装饰器装饰成tag，@register.inclusion_tag('comment/block.html')指定tag渲染的模板，方法return的context(dict)就是传入模板的参数。
5. 博客读>写，所以在写入时做markdown转换，可以用mistune也可以用markdown。
6. 新增uv、pv、RSS、SiteMap，其中统计uv和pv需要依据cookie中的uid，不存在的话可以由uid = uuid.uuid4().hex产生。
7. 在cookie中新增字段有response.set_cookie()方法，通过新增自定义middleware来实现。
8. CommonMix的get方法成为了非常简单的2步：super().get()和handle_visited()，在handle_visited()中处理pv和uv，update数据库时用到了F表达式。这里的逻辑是：用pv_key和uv_key来区别是否需要加1，如果请求中不带key，认为是新的请求，就要加1，否则表示key还没有过期，是旧的请求。加入key永不过期，也就是访问过再访问，永远不加1，但这是不符合pv和uv的意义。pv可以认为是分分钟过期，这1分钟访问和下1分钟访问，要算成2次访问，所以pv_key要在短时间内（比如1分钟）过期；而uv是同一天之内都算1次访问，第二天才算2次，所以设定uv_key在1天之后才过期。
9. @cached_property相当于@property的升级版，','.join(Post.tags.values_list('name', flat=True))是把多对多外键的所有值拿出来一起拼接成1个字符串。
