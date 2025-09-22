from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimePublishedMixin(models.Model):
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.'),
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        abstract = True


class Category(TimePublishedMixin):
    title = models.CharField(_('Заголовок'), max_length=256)
    description = models.TextField(_('Описание'))
    slug = models.SlugField(
        _('Идентификатор'),
        unique=True,
        help_text=_(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(TimePublishedMixin):
    name = models.CharField(_('Название места'), max_length=256)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(TimePublishedMixin):
    title = models.CharField(_('Заголовок'), max_length=256)
    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        help_text=_(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор публикации'),
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_('Местоположение'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    image = models.ImageField(_('Изображение'), upload_to='posts/', blank=True, null=True)

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        ordering = ('-pub_date', '-created_at')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Пост'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Автор'))
    text = models.TextField(_('Комментарий'))
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('комментарий')
        verbose_name_plural = _('Комментарии')

    def __str__(self):
        return f'Комментарий #{self.pk} к посту {self.post_id}'
