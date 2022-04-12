import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Comment, Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='testAuthor')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.author,
            text='Длинный тестовый пост',
            group=cls.group
        )

        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': f'{cls.post.id}'}
        )
        cls.POST_CREATE_URL = reverse('posts:post_create')
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': f'{cls.post.id}'}
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='testAuthorized')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_form_labels(self):
        """Проверяем, что label в полях формы PostForm
        совпадает с ожидаемым."""
        labels_data = {
            'text': 'Ваша запись',
            'group': 'Сообщество'
        }

        for field, label in labels_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostFormTests.form.fields[field].label,
                    label
                )

    def test_form_help_text(self):
        """Проверяем, что help_text в полях формы PostForm
        совпадает с ожидаемым."""
        help_texts_data = {
            'text': 'Пожалуйста, оставьте Вашу запись',
            'group': 'Пожалуйста, выберите Вашу группу',
        }

        for field, help_text in help_texts_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostFormTests.form.fields[field].help_text,
                    help_text
                )

    def count_posts(self):
        """Подсчитывает количество записей."""
        return Post.objects.count()

    def test_autorized_client_create_form(self):
        """Проверяем, что авторизованный пользователь
        создает запись c изображением."""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        test_image = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        post_aut_detail_url = reverse(
            'posts:profile', kwargs={'username': 'testAuthorized'}
        )
        create_form_data = {
            'text': 'Текст авторизованного пользователя',
            'group': PostFormTests.group.pk,
            'image': test_image
        }
        response = self.authorized_client.post(
            PostFormTests.POST_CREATE_URL,
            data=create_form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                text='Текст авторизованного пользователя',
                image='posts/small.gif'
            ).exists()
        )
        self.assertRedirects(response, post_aut_detail_url)
        self.assertEqual(self.count_posts(), 2)

    def test_guest_client_not_allowed_create_form(self):
        """Проверяем, что анонимный пользователь не создает запись в Post
        и перенаправляется на страницу /auth/login/ """
        post_guest_redirect_url = '/auth/login/?next=/create/'
        create_form_data = {
            'text': 'Текст анонимного пользователя',
        }
        response = self.guest_client.post(
            PostFormTests.POST_CREATE_URL,
            data=create_form_data,
            follow=True
        )
        self.assertFalse(
            Post.objects.filter(
                text='Текст анонимного пользователя',
            ).exists()
        )
        self.assertRedirects(response, post_guest_redirect_url)
        self.assertEqual(self.count_posts(), 1)

    def test_author_edit_form(self):
        """ Проверяем, что запись успешно редактируется автором."""
        edit_form_data = {
            'text': 'Отредактированный текст',
            'group': self.group.pk,
        }
        edit_response = self.author_client.post(
            PostFormTests.POST_EDIT_URL,
            data=edit_form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный текст',
            ).exists()
        )
        self.assertRedirects(edit_response, PostFormTests.POST_DETAIL_URL)
        self.assertEqual(self.count_posts(), 1)

    def test_autorized_not_allowed_edit_form(self):
        """ Проверяем, что зарегистрированный пользователь
        не может редактировать чужую запись."""
        edit_form_data = {
            'text': 'Коварно изменяю запись',
            'group': PostFormTests.group.pk
        }
        edit_response = self.authorized_client.post(
            PostFormTests.POST_EDIT_URL,
            data=edit_form_data,
            follow=True
        )
        self.assertFalse(
            Post.objects.filter(
                text='Коварно изменяю запись',
            ).exists()
        )
        self.assertRedirects(edit_response, PostFormTests.POST_DETAIL_URL)


class CommentFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='testAuthor')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            author=cls.author,
            text='Длинный тестовый пост',
            group=cls.group
        )

        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': f'{cls.post.id}'}
        )
        cls.COMMENT = reverse(
            'posts:add_comment', kwargs={'post_id': f'{cls.post.id}'}
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='testAuthorized')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_authorized_client_comments_post(self):
        """Проверяем, что авторизованный пользователь
        может комментировать записи"""
        comment_form_data = {'text': 'Длинный комментарий'}
        comment_response = self.authorized_client.post(
            CommentFormTests.COMMENT,
            data=comment_form_data,
            follow=True
        )
        self.assertTrue(
            Comment.objects.filter(text='Длинный комментарий').exists())
        self.assertRedirects(
            comment_response, CommentFormTests.POST_DETAIL_URL
        )
        self.assertEqual(Comment.objects.count(), 1)

    def test_guest_client_not_allowed_comment_post(self):
        """Проверяем, что незарегистрированный пользователь
        не может комментировать записи"""
        comment_guest_redirect_url = (
            f'/auth/login/?next=/posts/{CommentFormTests.post.id}/comment/'
        )
        comment_form_data = {'text': 'Комментарий гостя'}
        comment_response = self.guest_client.post(
            CommentFormTests.COMMENT,
            data=comment_form_data,
            follow=True
        )
        self.assertFalse(
            Comment.objects.filter(text='Комментарий гостя').exists())
        self.assertRedirects(
            comment_response, comment_guest_redirect_url
        )
        self.assertEqual(Comment.objects.count(), 0)
