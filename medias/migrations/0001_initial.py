# Generated by Django 3.2.16 on 2022-10-31 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaGenreMapping',
            fields=[
                ('mappingId', models.BigAutoField(primary_key=True, serialize=False)),
                ('createdBy', models.IntegerField()),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
                ('genreId', models.ForeignKey(db_column='genreId', on_delete=django.db.models.deletion.CASCADE, related_name='genremedia', to='core.genres')),
            ],
        ),
        migrations.CreateModel(
            name='MediaPeopleMapping',
            fields=[
                ('mappingId', models.BigAutoField(primary_key=True, serialize=False)),
                ('createdBy', models.IntegerField()),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medias',
            fields=[
                ('mediaId', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('mediaImagePath', models.CharField(blank=True, max_length=500, null=True)),
                ('authorName', models.CharField(max_length=200)),
                ('mediaType', models.IntegerField()),
                ('createdBy', models.IntegerField()),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
                ('modifiedBy', models.IntegerField()),
                ('modifiedOnUtc', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('genre', models.ManyToManyField(db_column='genreId', through='medias.MediaGenreMapping', to='core.Genres')),
                ('people', models.ManyToManyField(db_column='peopleId', through='medias.MediaPeopleMapping', to='people.Peoples')),
            ],
        ),
        migrations.CreateModel(
            name='SubMedias',
            fields=[
                ('subMediaId', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('imagePath', models.CharField(blank=True, max_length=500, null=True)),
                ('fileUrl', models.CharField(max_length=500)),
                ('viewsCount', models.IntegerField(default=0)),
                ('commentsCount', models.IntegerField(default=0)),
                ('likesCount', models.IntegerField(default=0)),
                ('dislikesCount', models.IntegerField(default=0)),
                ('createdBy', models.IntegerField()),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
                ('modifiedBy', models.IntegerField()),
                ('modifiedOnUtc', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('mediaId', models.ForeignKey(db_column='mediaId', on_delete=django.db.models.deletion.CASCADE, related_name='subMedias', to='medias.medias')),
            ],
        ),
        migrations.AddField(
            model_name='mediapeoplemapping',
            name='mediaId',
            field=models.ForeignKey(db_column='mediaId', on_delete=django.db.models.deletion.CASCADE, related_name='mediapeople', to='medias.medias'),
        ),
        migrations.AddField(
            model_name='mediapeoplemapping',
            name='peopleId',
            field=models.ForeignKey(db_column='peopleId', on_delete=django.db.models.deletion.CASCADE, related_name='peoplemedia', to='people.peoples'),
        ),
        migrations.AddField(
            model_name='mediagenremapping',
            name='mediaId',
            field=models.ForeignKey(db_column='mediaId', on_delete=django.db.models.deletion.CASCADE, related_name='mediagenre', to='medias.medias'),
        ),
    ]
