from django.shortcuts import render, get_object_or_404
from django.http import Http404

from datetime import datetime

from .models import Post, Category


def index(request):
    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True).order_by('-pub_date')[:5]
    return render(
        request=request,
        template_name='blog/index.html',
        context={'post_list': post_list}
    )


def post_detail(request, post_id):
    queryset = Post.objects.select_related('category').filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )
    post = get_object_or_404(queryset, pk=post_id)
    return render(
        request=request,
        template_name='blog/detail.html',
        context={'post': post}
    )


def category_posts(request, category_slug):
    context = dict()
    category = Category.objects.filter(slug=category_slug).first()
    if not category or not category.is_published:
        raise Http404
    context['category'] = category
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=datetime.now())
    context['post_list'] = post_list if post_list.exists else []
    return render(
        request=request,
        template_name='blog/category.html',
        context=context
    )
