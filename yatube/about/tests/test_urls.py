from http import HTTPStatus

from django.test import Client, TestCase

AUTOR = '/about/author/'
TECH = '/about/tech/'


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_existing_pages(self):
        """Проверяем, что страницы доступны любому пользователю
        и существуют."""
        any_urls_data = [AUTOR, TECH]

        for url in any_urls_data:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK
                )
