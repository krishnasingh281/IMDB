# Generated by Django 5.1.5 on 2025-01-27 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='WatchList',
            new_name='watchList',
        ),
    ]
