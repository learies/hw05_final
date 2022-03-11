from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.tests.data_for_test import (
    AUTHOR,
    SLUG,
    GROUP_TITLE,
    GROUP_DESCRIPTION,
    POST_TEXT,
    INDEX,
    PROFILE,
    GROUP_LIST,
)

NUMBER_PAGE = 10


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
            ) for i in range(NUMBER_PAGE)
        ])

    def setUp(self):
        self.guest_client = Client()

    def test_index_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse(INDEX)
        )
        self.assertEqual(len(response.context['page_obj']), NUMBER_PAGE)

    def test_group_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse(GROUP_LIST, kwargs={'slug': self.group.slug})
        )
        self.assertEqual(len(response.context['page_obj']), NUMBER_PAGE)

    def test_profile_page_contains_ten_records(self):
        response = self.guest_client.get(
            reverse(PROFILE, kwargs={'username': self.user})
        )
        self.assertEqual(len(response.context['page_obj']), NUMBER_PAGE)
