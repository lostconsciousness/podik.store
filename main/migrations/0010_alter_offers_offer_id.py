# Generated by Django 4.1.7 on 2023-04-14 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_offers_offer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='offer_id',
            field=models.CharField(max_length=255, null=True, verbose_name='Id замовлення'),
        ),
    ]