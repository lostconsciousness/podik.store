# Generated by Django 4.1.7 on 2023-04-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_podik_atomizer_volume_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filters',
            name='value',
            field=models.CharField(blank=True, max_length=255, verbose_name='Значення фільтру'),
        ),
    ]
