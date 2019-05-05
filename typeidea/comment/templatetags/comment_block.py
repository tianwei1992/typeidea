from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,    #  tagtemplate中不包含request对象，所以需要把tartget显示地传递进去
        'comment_form': CommentForm,
        'comment_list': Comment.get_by_target(target),
    }
