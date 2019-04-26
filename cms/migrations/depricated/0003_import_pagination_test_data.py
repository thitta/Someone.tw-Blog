from django.db import migrations

MOCK_TITLE = "__mock_post_for_test__"
MOCK_USER_ID = 3
MOCK_COLLECTION = {
    "DisplayName": "__mock_collection_for_test__",
    "IsPublic": True,
    "RankingIndex": 0
}


def add_mock_posts_and_collection(apps, schema_editor):
    Post = apps.get_model('cms', 'Post')
    Collection = apps.get_model("cms", "Collection")
    collection = Collection.objects.create(**MOCK_COLLECTION)
    for ind in range(0, 50):
        post = Post.objects.create(Title=MOCK_TITLE, Subtitle=f"{ind}", User_id=MOCK_USER_ID,
                                   BodyMarkdown="", BodyHTML="", IsPublic=True, IsOnList=True)
        collection.Posts.add(post)


def remove_all(apps, schema_editor):
    Post = apps.get_model('cms', 'Post')
    Collection = apps.get_model("cms", "Collection")
    Post.objects.filter(Title=MOCK_TITLE).delete()
    Collection.objects.filter(DisplayName=MOCK_COLLECTION["DisplayName"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0002_import_mock_user'),
    ]

    operations = [
        migrations.RunPython(add_mock_posts_and_collection, remove_all),
    ]
