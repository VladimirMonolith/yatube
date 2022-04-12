from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Класс для создания формы записи."""

    class Meta:
        model = Post

        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Ваша запись',
            'group': 'Сообщество',
        }
        help_texts = {
            'text': 'Пожалуйста, оставьте Вашу запись',
            'group': 'Пожалуйста, выберите Вашу группу',
        }


class CommentForm(forms.ModelForm):
    """Класс для создания формы комментария."""

    class Meta:
        model = Comment

        fields = ('text',)
        labels = {
            'text': 'Ваш комментарий',
        }
        help_texts = {
            'text': 'Пожалуйста, оставьте Ваш комментарий',
        }
