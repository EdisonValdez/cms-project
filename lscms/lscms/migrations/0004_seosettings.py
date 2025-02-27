# Generated by Django 5.1.6 on 2025-02-13 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lscms', '0003_alter_menuitem_options_and_more'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='SEOSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('meta_description', models.CharField(max_length=160)),
                ('meta_keywords', models.CharField(max_length=200)),
                ('og_title', models.CharField(blank=True, max_length=60)),
                ('og_description', models.CharField(blank=True, max_length=200)),
                ('canonical_url', models.URLField(blank=True)),
                ('robots_settings', models.CharField(choices=[('index,follow', 'Index and Follow'), ('noindex,follow', 'No Index but Follow'), ('index,nofollow', 'Index but No Follow'), ('noindex,nofollow', 'No Index and No Follow')], default='index,follow', max_length=50)),
                ('og_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'SEO Setting',
                'verbose_name_plural': 'SEO Settings',
            },
        ),
    ]
