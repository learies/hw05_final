from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.cache import cache

from posts.models import Post, Group, User
from posts.tests.data_test import (
    AUTHOR,
    SLUG,
    GROUP_TITLE,
    GROUP_DESCRIPTION,
    POST_TEXT,
    INDEX,
    INDEX_TEMPLATE,
    POST_CREATE,
    POST_EDIT,
    POST_CREATE_TEMPLATE,
    PROFILE,
    PROFILE_TEMPLATE,
    POST_DETAIL,
    POST_DETAIL_TEMPLATE,
    GROUP_LIST,
    GROUP_LIST_TEMPLATE,
)

NUBER_PAGE = 10


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
            group=cls.group,
        )
        cls.INDEX_PAGE = reverse(
            INDEX
        )
        cls.POST_DETAIL_PAGE = reverse(
            POST_DETAIL,
            kwargs={'post_id': cls.post.id}
        )
        cls.POST_EDIT_PAGE = reverse(
            POST_EDIT,
            kwargs={'post_id': cls.post.id}
        )
        cls.GROUP_LIST_PAGE = reverse(
            GROUP_LIST,
            kwargs={'slug': cls.group.slug}
        )
        cls.PROFILE_PAGE = reverse(
            PROFILE,
            kwargs={'username': cls.user}
        )
        cls.POST_CREATE_PAGE = reverse(
            POST_CREATE
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            self.INDEX_PAGE: INDEX_TEMPLATE,
            self.GROUP_LIST_PAGE: GROUP_LIST_TEMPLATE,
            self.PROFILE_PAGE: PROFILE_TEMPLATE,
            self.POST_DETAIL_PAGE: POST_DETAIL_TEMPLATE,
            self.POST_EDIT_PAGE: POST_CREATE_TEMPLATE,
            self.POST_CREATE_PAGE: POST_CREATE_TEMPLATE,
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                cache.clear()
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(POST_CREATE))
        form_fields = {
            'text': forms.fields.CharField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_context_post_detail(self):
        response = self.authorized_client.get(self.POST_DETAIL_PAGE)
        self.assertEqual(
            response.context.get('post').text, POST_TEXT
        )
        self.assertEqual(
            response.context.get('post').author.username, AUTHOR
        )
        self.assertEqual(
            response.context.get('post').group.title, GROUP_TITLE
        )
        self.assertEqual(
            response.context.get('post').group.description, GROUP_DESCRIPTION,
        )
        self.assertEqual(
            response.context.get('post').group.slug, SLUG
        )


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.bulk_create([
            Post(
                author=cls.user,
                text=f'{POST_TEXT} {i}',
                group=cls.group
            ) for i in range(NUBER_PAGE)
        ])

    def setUp(self):
        self.guest_client = Client()

    def test_index_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse(INDEX)
        )
        self.assertEqual(len(response.context['page_obj']), NUBER_PAGE)

    def test_group_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse(GROUP_LIST, kwargs={'slug': self.group.slug})
        )
        self.assertEqual(len(response.context['page_obj']), NUBER_PAGE)

    def test_profile_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse(PROFILE, kwargs={'username': self.user})
        )
        self.assertEqual(len(response.context['page_obj']), NUBER_PAGE)
