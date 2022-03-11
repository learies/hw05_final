from django.test import TestCase

from posts.models import Group, Post, User
from posts.tests.data_for_test import (
    AUTHOR,
    SLUG,
    GROUP_TITLE,
    GROUP_DESCRIPTION,
    POST_TEXT,
    PICTURE,
)


class PostModelTest(TestCase):
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
            image=PICTURE,
        )

    def test_models_have_correct_object_names_post(self):
        post = self.post
        object_names = post.text
        self.assertEqual(object_names, post.text[:15])

    def test_models_have_correct_object_names_group(self):
        group = self.group
        object_names = group.title
        self.assertEqual(object_names, str(group))

    def test_verbose_name(self):
        post = self.post
        field_verboses = {
            'text': 'Пост',
            'group': 'Группа',
            'image': 'Картинка',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        post = self.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
            'image': 'Загрузите картинку',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
