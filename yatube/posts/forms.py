from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Класс для создания формы записи."""

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Класс для создания формы комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
