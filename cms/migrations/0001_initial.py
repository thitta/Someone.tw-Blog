# Generated by Django 2.2 on 2019-04-17 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('PostId', models.AutoField(max_length=256, primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=256)),
                ('Subtitle', models.CharField(max_length=256)),
                ('BodyMarkdown', models.TextField()),
                ('BodyHTML', models.TextField()),
                ('CoverImageUrl', models.URLField(blank=True)),
                ('IsOnList', models.BooleanField(default=True)),
                ('IsPublic', models.BooleanField(default=True)),
                ('IsTop', models.BooleanField(default=False)),
                ('RankingIndex', models.IntegerField(default=0)),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('UpdateDate', models.DateTimeField(auto_now=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('DisplayName', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('Name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('CategoryName', models.CharField(max_length=32)),
                ('Value', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PostRelation',
            fields=[
                ('PostRelationId', models.AutoField(primary_key=True, serialize=False)),
                ('Ratio', models.FloatField()),
                ('FromPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ToPosts', to='cms.Post')),
                ('ToPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FromPosts', to='cms.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('CollectionId', models.AutoField(max_length=256, primary_key=True, serialize=False)),
                ('DisplayName', models.CharField(max_length=256)),
                ('IsPublic', models.BooleanField(default=True)),
                ('RankingIndex', models.IntegerField(default=0)),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('Posts', models.ManyToManyField(to='cms.Post')),
            ],
        ),
        migrations.AddIndex(
            model_name='postrelation',
            index=models.Index(fields=['Ratio'], name='cms_postrel_Ratio_394f9a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='postrelation',
            unique_together={('FromPost', 'ToPost')},
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['IsPublic'], name='cms_post_IsPubli_d664e2_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['IsTop'], name='cms_post_IsTop_c3bbaf_idx'),
        ),
    ]
