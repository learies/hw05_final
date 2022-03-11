import shutil

from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.forms import PostForm
from posts.tests.data_for_test import (
    AUTHOR,
    SLUG,
    GROUP_TITLE,
    GROUP_DESCRIPTION,
    POST_TEXT,
    CREATE_POST,
    POST_EDIT,
    PROFILE,
    TEMP_MEDIA_ROOT,
    PICTURE,
)


class PostCreateFormTests(TestCase):
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
            image=PICTURE
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': f'{POST_TEXT} 1',
            'group': self.group.id,
            'image': self.post.image,
        }
        response = self.authorized_client.post(
            reverse(CREATE_POST),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                PROFILE,
                kwargs={'username': self.user}
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=f'{POST_TEXT} 1',
                group=self.group,
            ).exists()
        )

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': f'{POST_TEXT} 1',
            'group': self.group.id,
            'image': self.post.image,
        }
        response = self.authorized_client.post(
            reverse(
                POST_EDIT,
                kwargs={'post_id': self.post.id},
            ),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(response.status_code, HTTPStatus.OK)
