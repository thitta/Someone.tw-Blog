from django.db import migrations, models

from ..utils import AuthorWidget

DEFAULT_ROWS = [  # (namespace, key, value)
    ("author", "enable", AuthorWidget.enable),
    ("author", "name", AuthorWidget.name),
    ("author", "image_url", AuthorWidget.image_url),
    ("author", "url", AuthorWidget.url),
    ("author", "description", AuthorWidget.description),
]


def add_default_rows(apps, schema_editor):
    SiteConfig = apps.get_model('cms', 'SiteConfig')
    for cfg in DEFAULT_ROWS:
        SiteConfig.objects.create(NameSpace=cfg[0], Key=cfg[1], Value=cfg[2])


def remove_default_rows(apps, schema_editor):
    SiteConfig = apps.get_model('cms', 'SiteConfig')
    for cfg in DEFAULT_ROWS:
        SiteConfig.objects.filter(NameSpace=cfg[0], Key=cfg[1], Value=cfg[2]).delete()


# -------------------- Migrations --------------------

class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SiteConfig',
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('ConfigId', models.AutoField(primary_key=True, serialize=False)),
                ('NameSpace', models.CharField(max_length=32)),
                ('Key', models.CharField(max_length=32)),
                ('Value', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddIndex(
            model_name='siteconfig',
            index=models.Index(fields=['NameSpace', 'Key'], name='cms_sitecon_NameSpa_045ac5_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='siteconfig',
            unique_together={('NameSpace', 'Key')},
        ),
        # add mock data
        migrations.RunPython(add_default_rows, remove_default_rows),
    ]
