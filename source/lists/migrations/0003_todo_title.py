# Generated by Django 3.1.2 on 2021-01-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20201215_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='title',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]
