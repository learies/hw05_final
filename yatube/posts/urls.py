from django.urls import path

from posts.views import (
    index,
    group_posts,
    profile,
    post_detail,
    post_create,
    post_edit,
    add_comment,
)

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('group/<slug:slug>/', group_posts, name='group_list'),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('posts/<post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
]
