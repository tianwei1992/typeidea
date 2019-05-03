from django.views.generic import ListView

from blog.views import CommonMixin
from .models import Link


class LinkListView(CommonMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'

