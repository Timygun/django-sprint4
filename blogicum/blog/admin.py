from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '—пусто—'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('name',)
    empty_value_display = '—пусто—'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'location',
                    'is_published', 'pub_date', 'created_at')
    list_filter = ('is_published', 'category', 'location', 'author')
    search_fields = ('title', 'text')
    date_hierarchy = 'pub_date'
    empty_value_display = '—пусто—'
