import random

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Article


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticlesView, self).get_context_data(**kwargs)
        context['random_articles'] = self.get_random_articles()
        return context

    def get_random_articles(self):
        return Article.objects.order_by('?')[:2]


class SingleView(DetailView):
    model = Article
    context_object_name = 'single'
    template_name = "single.html"


