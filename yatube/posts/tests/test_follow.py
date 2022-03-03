from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, User, Follow
from posts.tests.data_test import (
    AUTHOR,
    POST_TEXT,
    FOLLOW,
)

USER_2 = 'Ivan'


class PostFollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username=AUTHOR)
        cls.user_ivan = User.objects.create_user(username=USER_2)
        cls.post = Post.objects.create(
            author=cls.user_author,
            text=POST_TEXT,
        )
        cls.FOLLOW_INDEX = reverse('posts:follow_index')
        cls.FOLLOW = reverse(
            FOLLOW,
            kwargs={'username': cls.user_author},
        )
        cls.UNFOLLOW = reverse(
            'posts:profile_unfollow',
            kwargs={'username': cls.user_author},
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_ivan)

    def test_follow(self):
        """Проверка подписки на пользователя"""
        self.authorized_client.get(self.FOLLOW)
        self.assertTrue(Follow.objects.filter(
            user=self.user_ivan,
            author=self.user_author,
        ).exists())

    def test_unfollow(self):
        """Проверка отписки от пользователя"""
        Follow.objects.create(
            user=self.user_ivan,
            author=self.user_author,
        )
        self.authorized_client.get(self.UNFOLLOW, follow=True)
        self.assertFalse(Follow.objects.filter(
            user=self.user_ivan,
            author=self.user_author,
        ).exists())

    def test_view_post_followed_users(self):
        """Посты отображаются у подписанных людей"""
        Follow.objects.create(
            user=self.user_ivan,
            author=self.user_author,
        )
        response = self.authorized_client.get(self.FOLLOW_INDEX)
        context = response.context['page_obj']
        self.assertIn(self.post, context)

    def test_do_not_view_post_unfollowed_users(self):
        """Посты неотображаются у неподписанных людей"""
        authorized_client = Client()
        authorized_client.force_login(self.user_ivan)
        response_alex = authorized_client.get(self.FOLLOW_INDEX)
        self.assertNotIn(self.post, response_alex.context['page_obj'])
