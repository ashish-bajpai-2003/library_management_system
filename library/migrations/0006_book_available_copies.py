# Generated by Django 5.1.6 on 2025-03-19 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_bookissue'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='available_copies',
            field=models.IntegerField(default=1),
        ),
    ]
