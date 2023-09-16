# Generated by Django 3.2.16 on 2022-10-31 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exceptions',
            fields=[
                ('exceptionId', models.BigAutoField(primary_key=True, serialize=False)),
                ('stackTrace', models.TextField(blank=True, null=True)),
                ('message', models.CharField(blank=True, max_length=1000, null=True)),
                ('occuredOnUtc', models.DateTimeField(auto_now_add=True)),
                ('errorType', models.CharField(blank=True, max_length=1000, null=True)),
                ('exceptionMethod', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('genreId', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('genreImagePath', models.CharField(blank=True, max_length=500, null=True)),
                ('genreType', models.IntegerField()),
                ('createdBy', models.IntegerField()),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True)),
                ('modifiedBy', models.IntegerField()),
                ('modifiedOnUtc', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
    ]