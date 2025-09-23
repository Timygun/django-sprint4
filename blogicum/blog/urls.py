# blogicum/blog/urls.py
from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),

    path('profile/<str:username>/', views.profile, name='profile'),

    path('posts/create/', views.post_create, name='create_post'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='delete_post'),

    path('posts/<int:post_id>/comment/', views.comment_create, name='add_comment'),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.comment_edit,
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.comment_delete,
        name='delete_comment',
    ),
]
