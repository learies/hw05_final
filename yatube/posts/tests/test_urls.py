from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase, Client

from posts.models import Post, Group, User
from posts.tests.data_test import (
    AUTHOR,
    SLUG,
    GROUP_TITLE,
    GROUP_DESCRIPTION,
    POST_TEXT,
    INDEX_TEMPLATE,
    POST_CREATE_TEMPLATE,
    PROFILE_TEMPLATE,
    POST_DETAIL_TEMPLATE,
    GROUP_LIST_TEMPLATE,
)


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
        )
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.INDEX_URL = '/'
        cls.CREATE_POST_URL = '/create/'
        cls.EDIT_POST_URL = f'/posts/{cls.post.id}/edit/'
        cls.POST_DETAIL_URL = f'/posts/{cls.post.id}/'
        cls.PROFILE_URL = f'/profile/{cls.user}/'
        cls.GROUP_URL = f'/group/{cls.group.slug}/'
        cls.UNEXISTING_URL = '/unexisting_page/'

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_status_page_for_authorized_client(self):
        """Проверка доступности страницы для авторизованного пользователя"""
        client_url_status = {
            self.INDEX_URL: HTTPStatus.OK,
            self.POST_DETAIL_URL: HTTPStatus.OK,
            self.PROFILE_URL: HTTPStatus.OK,
            self.GROUP_URL: HTTPStatus.OK,
            self.CREATE_POST_URL: HTTPStatus.OK,
            self.EDIT_POST_URL: HTTPStatus.OK,
            self.UNEXISTING_URL: HTTPStatus.NOT_FOUND,
        }
        for url, status_code in client_url_status.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_status_page_for_guest_client(self):
        """Проверка доступности страницы для не авторизованного пользователя"""
        client_url_status = {
            self.CREATE_POST_URL: HTTPStatus.FOUND,
            self.EDIT_POST_URL: HTTPStatus.FOUND,
        }
        for url, status_code in client_url_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """Проверка доступности шаблона страницы по URL-адресу"""
        templates_url_names = {
            self.INDEX_URL: INDEX_TEMPLATE,
            self.GROUP_URL: GROUP_LIST_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.EDIT_POST_URL: POST_CREATE_TEMPLATE,
            self.CREATE_POST_URL: POST_CREATE_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                cache.clear()
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_urls_no_uses_template_for_guest_client(self):
        """
        Проверка не доступности шаблона страницы по URL-адресу для
        не авторизованного клиента.
        """
        templates_url_names = {
            self.CREATE_POST_URL: POST_CREATE_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateNotUsed(response, template)
