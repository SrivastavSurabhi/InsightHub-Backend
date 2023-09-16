# Generated by Django 3.2.16 on 2022-11-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('firstName', models.CharField(blank=True, max_length=30)),
                ('lastName', models.CharField(blank=True, max_length=30)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True, unique=True)),
                ('isActive', models.BooleanField(default=True)),
                ('userRole', models.IntegerField(choices=[(1, 'admin'), (2, 'user')], default=2)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('createdBy', models.IntegerField(default=1)),
                ('createdOnUtc', models.DateTimeField(auto_now_add=True, null=True)),
                ('modifiedBy', models.IntegerField(default=1)),
                ('modifiedOnUtc', models.DateTimeField(auto_now=True)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]