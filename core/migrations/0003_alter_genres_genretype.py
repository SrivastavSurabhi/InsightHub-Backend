# Generated by Django 3.2.16 on 2022-11-16 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='genreType',
            field=models.IntegerField(choices=[(1, 'People'), (2, 'Media')]),
        ),
    ]
