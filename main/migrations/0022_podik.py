# Generated by Django 4.1.7 on 2023-05-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_cashbackpercentage_delete_podik_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Podik',
            fields=[
                ('name', models.CharField(max_length=255, verbose_name='Назва продукту')),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('available', models.BooleanField(verbose_name='Доступність')),
                ('price', models.IntegerField(verbose_name='Ціна')),
                ('currencyId', models.CharField(max_length=255, verbose_name='Валюта')),
                ('categoryId', models.IntegerField(verbose_name='Id категорії')),
                ('vendorCode', models.IntegerField()),
                ('quantity_in_stock', models.IntegerField(verbose_name='Кількість товару склад')),
                ('url', models.CharField(max_length=255)),
                ('picture', models.CharField(max_length=255, verbose_name='URL картинки')),
                ('param', models.TextField(null=True)),
                ('flavour', models.CharField(max_length=255, null=True, verbose_name='Вибір смаку')),
                ('nicotine_strength', models.CharField(max_length=255, null=True, verbose_name='Міцність нікотину')),
                ('fluid_volume', models.CharField(max_length=255, null=True, verbose_name='Обсяг рідини')),
                ('battery_capacity', models.CharField(max_length=255, null=True, verbose_name='Ємність акумулятора')),
                ('cartridge_capacity', models.CharField(max_length=255, null=True, verbose_name="Об'єм картриджа")),
                ('resistance', models.CharField(max_length=255, null=True, verbose_name='Вибір опору')),
                ('power', models.CharField(max_length=255, null=True, verbose_name='Потужність')),
                ('atomizer_volume', models.CharField(max_length=255, null=True, verbose_name='Обсяг атомайзера')),
                ('max_power', models.CharField(max_length=255, null=True, verbose_name='Максимальна потужність')),
                ('puffs_number', models.CharField(max_length=255, null=True, verbose_name='Кількість затяжок')),
                ('rechargeable', models.BooleanField(null=True, verbose_name="Перезаряджаються'")),
                ('compatibility_selection', models.CharField(max_length=255, null=True, verbose_name='Вибір сумісності')),
            ],
            options={
                'verbose_name': 'Електронна цигарка',
                'verbose_name_plural': 'Електронні цигарки',
                'ordering': ['categoryId', 'name'],
            },
        ),
    ]
