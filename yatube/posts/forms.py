from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Класс для создания формы записи."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = (
            'Здесь Вы можете оставить Вашу запись'
        )
        self.fields['group'].empty_label = (
            'Здесь Вы можете выбрать сообщество'
        )

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Класс для создания формы комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
