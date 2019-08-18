from django.db import migrations, models

# -------------------- Add mock config --------------------

SITE_CONFIGS = [
    {
        "NameSpace": "author",
        "Key": "name",
        "Value": "John Smith"
    },
    {
        "NameSpace": "author",
        "Key": "description",
        "Value": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s"
    }
]


def add_config_data(apps, schema_editor):
    SiteConfig = apps.get_model('cms', 'SiteConfig')
    for cfg in SITE_CONFIGS:
        SiteConfig.objects.create(**cfg)


def remove_config_data(apps, schema_editor):
    SiteConfig = apps.get_model('cms', 'SiteConfig')
    for cfg in SITE_CONFIGS:
        SiteConfig.objects.filter(NameSpace=cfg["NameSpace"], Key=cfg["Key"], Value=cfg["Value"]).delete()


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
        migrations.RunPython(add_config_data, remove_config_data),
    ]
