import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

AUTHOR = 'auth'
SLUG = 'test-slug'
GROUP_TITLE = 'Тестовая группа'
GROUP_DESCRIPTION = 'Тестовое описание'
POST_TEXT = 'Тестовая пост'

INDEX = 'posts:index'
INDEX_TEMPLATE = 'posts/index.html'

CREATE_POST = 'posts:post_create'
POST_EDIT = 'posts:post_edit'
CREATE_POST_TEMPLATE = 'posts/create_post.html'

PROFILE = 'posts:profile'
PROFILE_TEMPLATE = 'posts/profile.html'

POST_DETAIL = 'posts:post_detail'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'

GROUP_LIST = 'posts:group_list'
GROUP_LIST_TEMPLATE = 'posts/group_list.html'

FOLLOW = 'posts:profile_follow'
FOLLOW_TEMPLATE = 'posts/follow.html'

TEMPLATE_404 = 'core/404.html'

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

PICTURE = SimpleUploadedFile(
    name='small.gif',
    content=(
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
    ),
    content_type='image/gif'
)
