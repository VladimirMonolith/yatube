from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

AUTOR_URL = reverse('about:author')
TECH_URL = reverse('about:tech')


class AboutViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_pages_accessible_by_name(self):
        """Проверяем, что URL, генерируемый при помощи
        имени namespace:name, доступен."""

        for reverse_url in [AUTOR_URL, TECH_URL]:
            with self.subTest(reverse_url=reverse_url):
                response = self.guest_client.get(reverse_url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK
                )

    def test_about_pages_use_correct_templates(self):
        """Проверяем, что view-классы используют ожидаемые шаблоны."""
        templates_reverse_data = {
            AUTOR_URL: 'about/author.html',
            TECH_URL: 'about/tech.html',
        }

        for reverse_url, template in templates_reverse_data.items():
            with self.subTest(reverse_url=reverse_url):
                response = self.guest_client.get(reverse_url)
                self.assertTemplateUsed(
                    response,
                    template
                )
