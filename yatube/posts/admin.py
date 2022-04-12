from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс настройки раздела записей."""

    list_display = (
        'pk',
        'text',
        'image',
        'pub_date',
        'author',
        'group',
        'count_comments',
    )
    empty_value_display = '-пусто-'
    list_editable = ('group',)
    list_filter = ('pub_date',)
    list_per_page = 10
    search_fields = ('text',)

    def count_comments(self, object):
        return object.comments.count()

    count_comments.short_description = 'Количество комментариев'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Класс настройки раздела сообществ."""

    list_display = (
        'pk',
        'title',
        'slug',
        'description',
        'count_posts'
    )
    empty_value_display = '-пусто-'
    list_filter = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def count_posts(self, object):
        return object.posts.count()

    count_posts.short_description = 'Количество записей'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk',
        'post',
        'author',
        'text',
        'created'
    )

    list_editable = ('author',)
    list_filter = ('author',)
    list_per_page = 10
    search_fields = ('text',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Класс настройки раздела подписок."""

    list_display = (
        'pk',
        'author',
        'user',
    )

    list_editable = ('author',)
    list_filter = ('author',)
    list_per_page = 10
    search_fields = ('author',)


admin.site.site_title = 'Администрирование Yatube'
admin.site.site_header = 'Администрирование Yatube'
