# Generated by Django 3.2.5 on 2021-11-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(blank=True, upload_to='avatars/'),
        ),
    ]
