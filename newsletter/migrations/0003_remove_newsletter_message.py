# Generated by Django 3.2.11 on 2022-02-05 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_alter_newsletter_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='message',
        ),
    ]
