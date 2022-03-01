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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_status_page(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_status_page_for_authorized(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_slug_status_page(self):
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_slug_status_page_for_authorized(self):
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_username_status_page(self):
        response = self.guest_client.get(f'/profile/{self.user}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_username_status_page_for_authorized(self):
        response = self.guest_client.get(f'/profile/{self.user}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_id_status_page(self):
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_id_status_page_for_authorized(self):
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_status_page(self):
        response = self.guest_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_edit_status_page_for_authorized(self):
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_status_page(self):
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_create_status_page_for_authorized(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_status_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_unexisting_status_page(self):
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': INDEX_TEMPLATE,
            f'/group/{self.group.slug}/': GROUP_LIST_TEMPLATE,
            f'/profile/{self.user}/': PROFILE_TEMPLATE,
            f'/posts/{self.post.id}/': POST_DETAIL_TEMPLATE,
            f'/posts/{self.post.id}/edit/': POST_CREATE_TEMPLATE,
            '/create/': POST_CREATE_TEMPLATE,
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                cache.clear()
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
