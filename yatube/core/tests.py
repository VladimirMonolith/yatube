from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class ViewTestClass(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='testAuthorized')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def assertions(self, response):
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')

    def test_guest_error_page(self):
        response = self.guest_client.get('/nonexist-page/')
        self.assertions(response)

    def test_aut_error_page(self):
        response = self.authorized_client.get('/nonexist-page/')
        self.assertions(response)
