from datetime import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Category


def index(request):
    post_list = get_base_queryset()[:5]
    return render(
        request=request,
        template_name='blog/index.html',
        context={'post_list': post_list}
    )


def post_detail(request, post_id):
    post = get_object_or_404(get_base_queryset(), pk=post_id)
    return render(
        request=request,
        template_name='blog/detail.html',
        context={'post': post}
    )


def category_posts(request, category_slug):
    context = dict()
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_base_queryset().filter(category=category)
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(
        request=request,
        template_name='blog/category.html',
        context=context
    )


def get_base_queryset():
    return Post.objects.select_related(
        'category',
        'author',
        'location'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )
