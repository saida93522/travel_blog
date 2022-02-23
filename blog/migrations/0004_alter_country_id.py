# Generated by Django 3.2.11 on 2022-02-23 21:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comment_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
