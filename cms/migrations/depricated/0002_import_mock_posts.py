from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.contrib.auth import get_user_model
from cms.utils import reset_post_relations, set_post_relations

USER = {
    "username": "tester",
    "password": "(secret)",
}

PROFILE = {
    "DisplayName": "Someone Robot"
}

POSTS = [
    {
        "Title": "Hello World",
        "Subtitle": "Official Document",
        "BodyMarkdown": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin accumsan dapibus neque, et luctus turpis feugiat sit amet. Duis ut eros iaculis, tincidunt ligula in, ultricies lorem. Mauris aliquet maximus sapien vitae porta.",
        "BodyHTML": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin accumsan dapibus neque, et luctus turpis feugiat sit amet. Duis ut eros iaculis, tincidunt ligula in, ultricies lorem. Mauris aliquet maximus sapien vitae porta.",
        "CoverImageUrl": "/static/cms/img/helloworld.jpg",
        "IsOnList": True,
        "IsPublic": True,
        "IsTop": False,
        "RankingIndex": 0,
    },
    {
        "Title": "About",
        "Subtitle": "Official Document",
        "BodyMarkdown": "Lorem ipsum dolor sit amet.",
        "BodyHTML": "Lorem ipsum dolor sit amet.",
        "CoverImageUrl": "",
        "IsOnList": False,
        "IsPublic": True,
        "IsTop": False,
        "RankingIndex": 0,
    },
    {
        "Title": "Copyright",
        "Subtitle": "Official Document",
        "BodyMarkdown": "Lorem ipsum dolor sit amet.",
        "BodyHTML": "Lorem ipsum dolor sit amet.",
        "CoverImageUrl": "",
        "IsOnList": False,
        "IsPublic": True,
        "IsTop": False,
        "RankingIndex": 0,
    },
]

COLLECTION = {
    "DisplayName": "Default Collection",
    "IsPublic": True,
    "RankingIndex": 0
}


def add_user_data(apps, schema_editor):
    User = get_user_model()
    Profile = apps.get_model('cms', 'Profile')
    try:
        user = User.objects.get(username=USER["username"])
    except ObjectDoesNotExist:
        user = User.objects.create_user(username=USER["username"], password=USER["password"])
    try:
        # for unknown reason, fetch profile with User=user returns error
        # it seems related to __fake__ object
        # so we use User_id=user.id
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
    Post = apps.get_model('cms', 'Post')
    User = get_user_model()
    user = User.objects.get(username=USER["username"])
    for POST in POSTS:
        Post.objects.create(User_id=user.id, **POST)
        reset_post_relations()


def add_collection_data(apps, schema_editor):
    Collection = apps.get_model('cms', 'Collection')
    Post = apps.get_model('cms', 'Post')
    collection = Collection.objects.create(**COLLECTION)
    posts = Post.objects.filter(**POSTS[0])
    for POST in POSTS[1:]:
        posts = posts | Post.objects.filter(**POST)
    collection.Posts.add(*posts)


def remove_collection_data(apps, schema_editor):
    Collection = apps.get_model('cms', 'Collection')
    Collection.objects.filter(**COLLECTION).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user_data, remove_user_data),
        migrations.RunPython(add_post_data, remove_user_data),
        migrations.RunPython(add_collection_data, remove_collection_data),
    ]
