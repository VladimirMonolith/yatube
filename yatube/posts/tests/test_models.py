from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='testAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Длинный тестовый пост',
            group=cls.group
        )

        cls.LENGTH_TEXT = 15

    def test_model_post_have_correct_str_text(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        post_text = post.text[:PostModelTest.LENGTH_TEXT]
        self.assertEqual(str(post), post_text)

    def test_model_group_have_correct_str_title(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = PostModelTest.group
        group_title = group.title
        self.assertEqual(str(group), group_title)

    def test_post_verbose_name(self):
        """Проверяем, что verbose_name в полях модели Post
        совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Запись',
            'pub_date': 'Дата публикации',
            'author': 'автор',
            'group': 'Сообщество',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name,
                    expected
                )

    def test_group_verbose_name(self):
        """Проверяем, что verbose_name в полях модели Group
        совпадает с ожидаемым."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Название сообщества',
            'slug': 'адрес',
            'description': 'описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name,
                    expected
                )

    def test_post_help_text(self):
        """Проверяем, что help_text в полях модели Post
        совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help = {
            'text': 'Пожалуйста, оставьте Вашу запись',
            'group': 'Пожалуйста, выберите Вашу группу'
        }
        for value, expected in field_help.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text,
                    expected
                )
