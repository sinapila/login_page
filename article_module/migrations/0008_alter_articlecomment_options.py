# Generated by Django 4.0.3 on 2022-04-09 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0007_articlecomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
    ]