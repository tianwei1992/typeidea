from __future__ import unicode_literals

from pprint import pprint as pp

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import F, Q, Count, Sum
from django.test import TestCase
from django.test.utils import override_settings

from .models import Category, Post


class TestCategory(TestCase):
    @override_settings(DEBUG=True)
    def setUp(self):
        self.user = user = User.objects.create_user('the5fire', 'fake@email.com', 'password')
        Category.objects.bulk_create([
            Category(name='cate_bulk_%s' % i, owner=user)
            for i in range(10)
        ])

    @override_settings(DEBUG=True)
    def test_filter(self):
        categories = Category.objects.filter(
            (Q(id=1) & Q(id=2))
        )
        print(categories)
        print('===' * 10)

        user = User.objects.annotate(cate_sum=Sum('category__status')).get(username="the5fire")
        self.assertEqual(user.cate_sum, 10, '总计是10')

        category = Category.objects.filter(id=1).update(status=F('status') + 1)

        print(user.cate_sum)
        self.assertEqual(user.cate_sum, 11, '总计11')
        pp(connection.queries)
