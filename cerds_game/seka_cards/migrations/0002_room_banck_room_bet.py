# Generated by Django 5.1.1 on 2025-01-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seka_cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='banck',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='bet',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
