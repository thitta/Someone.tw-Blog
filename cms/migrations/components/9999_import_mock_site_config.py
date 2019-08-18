from django.db import migrations

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

DEPENDENCIES = "0002_rebuild_siteconfig"


# -------------------- MIGRATION CODE --------------------

def add_config_data(apps, schema_editor):
    SiteConfig = apps.get_model('cms', 'SiteConfig')
    for cfg in SITE_CONFIGS:
        SiteConfig.objects.create(**cfg)


def remove_config_data(apps, schema_editor):
    SiteConfig = apps.get_model('cms', 'SiteConfig')
    for cfg in SITE_CONFIGS:
        SiteConfig.objects.filter(NameSpace=cfg["NameSpace"], Key=cfg["Key"], Value=cfg["Value"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('cms', DEPENDENCIES),
    ]

    operations = [
        migrations.RunPython(add_config_data, remove_config_data),
    ]
