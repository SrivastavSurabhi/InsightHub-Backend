# Generated by Django 4.1.2 on 2022-11-15 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_rename_mediaid_submedias_medias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medias',
            name='mediaType',
            field=models.IntegerField(choices=[(1, 'Audio'), (2, 'Video'), (2, 'Podcast')]),
        ),
    ]
