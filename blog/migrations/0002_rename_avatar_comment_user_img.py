# Generated by Django 3.2.11 on 2022-02-20 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='avatar',
            new_name='user_img',
        ),
    ]