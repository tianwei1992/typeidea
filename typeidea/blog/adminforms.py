# coding:utf-8

from django import forms


class PostAdminForm(forms.ModelForm):
    """填充ModelAdmin类的form属性，用于定制各字段在页面的展示样式)
    用法：
        class PostAdmin(admin.ModelAdmin):
            form = PostAdminForm
    """
    status = forms.BooleanField(label="是否删除", required=True)  # TODO: 处理布尔类型为我们需要的字段
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
