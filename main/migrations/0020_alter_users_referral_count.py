# Generated by Django 4.1.7 on 2023-04-28 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_offers_call'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='referral_count',
            field=models.IntegerField(null=True, verbose_name='Кількість рефералів'),
        ),
    ]
