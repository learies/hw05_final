from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

ABOUT_URL = reverse('about:author')
ABOUT_TEMPLATE = 'about/author.html'

TECH_URL = reverse('about:tech')
TECH_TEMPLATE = 'about/tech.html'


class AboutURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_about_author_status_page(self):
        response = self.guest_client.get(ABOUT_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_tech_status_page(self):
        response = self.guest_client.get(TECH_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class AboutViewsTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_pages_uses_correct_template(self):
        templates = {
            ABOUT_URL: ABOUT_TEMPLATE,
            TECH_URL: TECH_TEMPLATE,
        }
        for url, template in templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
