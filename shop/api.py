# coding: utf-8

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from shop.models import Category


class CategoryResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'parent': 'parent_id',
        'count': 'count',
        'order': 'order',
        'date': 'date'
    })

    def list(self):
        return Category.objects.all()

    def detail(self, slug):
        return Category.objects.get(slug=slug)


