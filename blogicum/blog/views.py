from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Category, Post

POSTS_PER_PAGE = 10


def published_filter():
    """Базовый QuerySet для опубликованных постов (видимых всем)."""
    now = timezone.now()
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=now,
        category__is_published=True,
    )


def _paginate(request, queryset):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    qs = published_filter().select_related('author', 'category', 'location')
    page_obj = _paginate(request, qs)
    context = {
        'page_obj': page_obj,
        'post_list': page_obj.object_list,
    }
    return render(request, 'blog/index.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    qs = (
        published_filter()
        .filter(category=category)
        .select_related('author', 'category', 'location')
    )
    page_obj = _paginate(request, qs)
    context = {
        'category': category,
        'page_obj': page_obj,
        'post_list': page_obj.object_list,
    }
    return render(request, 'blog/category.html', context)


def profile(request, username):
    User = get_user_model()
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated and request.user == author:
        qs = Post.objects.filter(author=author).select_related(
            'author',
            'category',
            'location',
        )
    else:
        qs = published_filter().filter(author=author).select_related(
            'author',
            'category',
            'location',
        )
    page_obj = _paginate(request, qs)
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_list': page_obj.object_list,
    }
    return render(request, 'blog/profile.html', context)


def post_detail(request, pk):
    """Детальная: автор видит свой пост всегда; остальные — опубликованные."""
    base_qs = Post.objects.select_related('author', 'category', 'location')
    if request.user.is_authenticated:
        try:
            post = base_qs.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            post = get_object_or_404(
                published_filter().select_related(
                    'author',
                    'category',
                    'location',
                ),
                pk=pk,
            )
    else:
        post = get_object_or_404(
            published_filter().select_related(
                'author',
                'category',
                'location',
            ),
            pk=pk,
        )

    form = CommentForm() if request.user.is_authenticated else None
    comments = post.comments.select_related('author').all()
    return render(
        request,
        'blog/detail.html',
        {'post': post, 'form': form, 'comments': comments},
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form, 'is_edit': False})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_id)
    return render(
        request,
        'blog/create.html',
        {'form': form, 'is_edit': True, 'post': post},
    )


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'post': post, 'is_delete': True})


@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=post_id)


@login_required
def comment_edit(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(post.comments, pk=comment_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_id)
    return render(
        request,
        'blog/create.html',
        {
            'form': form,
            'post': post,
            'comment': comment,
            'is_edit_comment': True,
        },
    )


@login_required
def comment_delete(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(post.comments, pk=comment_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', pk=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=post_id)
    return render(
        request,
        'blog/create.html',
        {'post': post, 'comment': comment, 'is_delete_comment': True},
    )
