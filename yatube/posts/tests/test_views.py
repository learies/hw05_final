from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.cache import cache

from posts.models import Post, Group, User
from posts.tests.data_for_test import (
    AUTHOR,
    SLUG,
    GROUP_TITLE,
    GROUP_DESCRIPTION,
    POST_TEXT,
    INDEX,
    INDEX_TEMPLATE,
    CREATE_POST,
    POST_EDIT,
    CREATE_POST_TEMPLATE,
    PROFILE,
    PROFILE_TEMPLATE,
    POST_DETAIL,
    POST_DETAIL_TEMPLATE,
    GROUP_LIST,
    GROUP_LIST_TEMPLATE,
)


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
            CREATE_POST
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверка доступности шаблона страницы по URLs-адресу"""
        templates_pages_names = {
            self.INDEX_PAGE: INDEX_TEMPLATE,
            self.GROUP_LIST_PAGE: GROUP_LIST_TEMPLATE,
            self.PROFILE_PAGE: PROFILE_TEMPLATE,
            self.POST_DETAIL_PAGE: POST_DETAIL_TEMPLATE,
            self.POST_EDIT_PAGE: CREATE_POST_TEMPLATE,
            self.POST_CREATE_PAGE: CREATE_POST_TEMPLATE,
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                cache.clear()
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_create_show_correct_context(self):
        response = self.authorized_client.get(self.POST_CREATE_PAGE)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.ChoiceField,
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

    def test_cache_function_in_page_index(self):
        response_1 = self.guest_client.get(self.INDEX_PAGE)
        response_obj_content_1 = response_1.content
        response_1.context['page_obj'][0].delete()
        form_data = {
            'text': POST_TEXT,
        }
        self.authorized_client.post(
            self.POST_CREATE_PAGE,
            data=form_data,
            follow=True
        )
        response_2 = self.guest_client.get(self.INDEX_PAGE)
        response_obj_content_2 = response_2.content
        self.assertEqual(response_obj_content_1, response_obj_content_2)
        cache.clear()
        response_3 = self.guest_client.get(self.INDEX_PAGE)
        response_obj_content_3 = response_3.content
        self.assertNotEqual(
            response_obj_content_2, response_obj_content_3)
