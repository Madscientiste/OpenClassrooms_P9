# Generated by Django 3.2.5 on 2021-11-12 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20211111_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='description',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='title',
            new_name='headline',
        ),
    ]
