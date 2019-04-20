## version 0.1.0 -- 2019-04-17

init project

## Finish Chatper 5 & 6 -- 2019-04-20

    完成了Model和Admin。Model是一切的基础，Admin就是管理Model在页面上的呈现。
1.  Model字段还有IntegerField带choices属性，null设定数据库层面允许为空，blank设定业务层面。
2.  QuerySet是核心对象：懒加载和链式调用；Django还封装了F表达式、Q表达式、Count、Sum来支持聚合。
3.  Admin做的比较多，最简单可以继承admin.ModelAdmin然后通过注册与某个Model绑定，如果想要个性化可以定制list_fields, fields, fieldsets等等特性，还可以重载save_model()和get_query()方法，在每次保存时自动用request.user填充onwner名字。其中fields的元素既可以是Model原有的字段，也可以由具有某种处理过程的自定义字段, 比如def operator(self, obj)以及def post_count(self, obj)。这些字段本质上是方法。
4.  对Admin的定制分成3类，定制这个字段怎么显示，比如定制form特性(自定义class ModelForm然后将实例赋值给form字段)；定制字段的内容，比如定制fileter特性；定制字段显示的布局和位置，fieldset特定，inline特性。
5.  不同url路由到不同site分配不同内容：创建AdminSite实例，然后分配内容。
