# Generated by Django 4.1.7 on 2023-05-01 19:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_users_referral_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashbackPercentage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Процент кешбека')),
            ],
            options={
                'verbose_name': 'Процент кешбека',
                'verbose_name_plural': 'Процент кешбека',
            },
        ),
        migrations.DeleteModel(
            name='Podik',
        ),
        migrations.RemoveField(
            model_name='areas_and_costs',
            name='cost',
        ),
        migrations.AddField(
            model_name='areas_and_costs',
            name='cost_for_adress',
            field=models.IntegerField(default=0, verbose_name='Ціна за доставку за адресою'),
        ),
        migrations.AddField(
            model_name='areas_and_costs',
            name='cost_for_post',
            field=models.IntegerField(default=0, verbose_name='Ціна за доставку у поштомат'),
        ),
        migrations.AddField(
            model_name='areas_and_costs',
            name='cost_for_warehouse',
            field=models.IntegerField(default=0, verbose_name='Ціна за доставку у відділення'),
        ),
        migrations.AddField(
            model_name='offers',
            name='novapost_en',
            field=models.CharField(max_length=255, null=True, verbose_name='ТТН'),
        ),
        migrations.AddField(
            model_name='users',
            name='cashback_amount',
            field=models.IntegerField(default=0, verbose_name='Кешбек'),
        ),
    ]
