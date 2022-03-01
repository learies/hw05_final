from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from posts.forms import PostForm, CommentForm
from posts.models import Group, Post, User
from posts.paginator import get_paginator


@cache_page(20, key_prefix='index_page')
def index(request):
    # if 'index_page' in cache:
    #     posts = cache.get('index_page')
    # else:
    #     posts = Post.objects.all()
    #     cache.set('index_page', posts, 20)
    posts = Post.objects.all()
    page_obj = get_paginator(request, posts)
    context = {
        'title': 'Последние обновления на сайте',
        'posts': posts,
        'page_obj': page_obj,
    }
    cache.clear()
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group.all()
    page_obj = get_paginator(request, posts)
    context = {
        'title': f'Записи сообщества {group.title}',
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    page_obj = get_paginator(request, posts)
    context = {
        'title': f'{user.get_full_name()} профайл пользователя',
        'author': user,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = User.objects.get(username=post.author.username)
    form = CommentForm(request.POST or None)
    context = {
        'title': post.text[:30],
        'post': post,
        'author_posts': Post.objects.filter(author=author),
        'comments': post.comments.all(),
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
        return render(request, 'posts/create_post.html', {'form': form})
    context = {
        'title': 'Добавить запись',
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'title': 'Редактировать запись',
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
