# Generated by Django 4.1.7 on 2023-04-28 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_users_message_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='call',
            field=models.BooleanField(null=True, verbose_name='Дзвонити'),
        ),
    ]
