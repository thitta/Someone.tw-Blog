import markdown
import os
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.contrib.auth import get_user_model
from cms.utils import reset_post_relations
from metapost import MetaPostReader
from markdown.extensions.extra import ExtraExtension

MOCKS_DIRPATH = os.path.join(os.path.dirname(__file__), "mocks")

USER = {
    "username": "tester",
    "password": "(secret)",
}

PROFILE = {
    "DisplayName": "Someone Robot"
}

COLLECTIONS = [
    {
        "DisplayName": "Python Lucid Showcase",
        "IsPublic": True,
        "RankingIndex": 0
    },
    {
        "DisplayName": "Gaming Small Talks",
        "IsPublic": True,
        "RankingIndex": 0
    },
    {
        "DisplayName": "Empty Collection",
        "IsPublic": True,
        "RankingIndex": -1
    },
]


def add_user_data(apps, schema_editor):
    User = get_user_model()
    Profile = apps.get_model('cms', 'Profile')
    # create or get user
    try:
        user = User.objects.get(username=USER["username"])
    except ObjectDoesNotExist:
        user = User.objects.create_user(username=USER["username"], password=USER["password"])
    # create or get profile
    try:
        Profile.objects.get(User_id=user.id)
    except ObjectDoesNotExist:
        Profile.objects.create(User_id=user.id, DisplayName=PROFILE["DisplayName"])


def remove_user_data(apps, schema_editor):
    User = get_user_model()
    try:
        User.objects.get(username=USER["username"]).delete()
    except ObjectDoesNotExist:
        pass


def add_post_data(apps, schema_editor):
    # create user
    Post = apps.get_model('cms', 'Post')
    User = get_user_model()
    user = User.objects.get(username=USER["username"])
    # parse posts via MetaPostReader
    mtpr = MetaPostReader()
    mtpr.set_strict_mode(False)
    mtpr.add_meta_cfg("Title", "str", True)
    mtpr.add_meta_cfg("Subtitle", "str", True)
    mtpr.add_meta_cfg("CoverImageUrl", "str", False, "")
    mtpr.add_meta_cfg("IsOnList", "bool", True)
    mtpr.add_meta_cfg("IsPublic", "bool", True)
    mtpr.add_meta_cfg("IsTop", "bool", True)
    mtpr.add_meta_cfg("RankingIndex", "int", True)
    posts = mtpr.read_dir(dirpath=MOCKS_DIRPATH, reset=True, walk=False).to_meta()
    # manipulate data to ORM format
    for post in posts:
        post["User_id"] = user.id
        post["BodyMarkdown"] = post.pop("_content_markdown_")
        post["BodyHTML"] = markdown.markdown(post["BodyMarkdown"],
                                             extensions=[ExtraExtension()])
        post.pop("_filepath_")
        post.pop("_filename_")
        post.pop("_last_update_")
    # import
    Post.objects.bulk_create([Post(**p) for p in posts])
    # build posts for pagination
    for ind in range(0, 20):
        post = Post.objects.create(Title=f"Posts-{ind + 1} for Pagination Testing", Subtitle=f"Pagination Testing",
                                   User_id=user.id,
                                   BodyMarkdown="This is a post for pagination testing",
                                   BodyHTML="<p>This is a post for pagination testing</p>",
                                   IsPublic=True, IsOnList=True, RankingIndex=-1)
    reset_post_relations()


def add_collection_data(apps, schema_editor):
    Collection = apps.get_model('cms', 'Collection')
    collections = [Collection(**c) for c in COLLECTIONS]
    Collection.objects.bulk_create(collections)


def remove_collection_data(apps, schema_editor):
    Collection = apps.get_model('cms', 'Collection')
    for collection in COLLECTIONS:
        Collection.objects.filter(**collection).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user_data, remove_user_data),
        migrations.RunPython(add_post_data, remove_user_data),
        migrations.RunPython(add_collection_data, remove_collection_data),
    ]
