from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Podik(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва продукту")
    id = models.CharField(max_length=255, primary_key=True)
    available = models.BooleanField(verbose_name="Доступність")
    price = models.IntegerField(verbose_name="Ціна")
    currencyId = models.CharField(max_length=255, verbose_name="Валюта")
    categoryId = models.IntegerField(verbose_name="Id категорії")
    vendorCode = models.IntegerField()
    quantity_in_stock = models.IntegerField(verbose_name="Кількість товару склад")
    url = models.CharField(max_length=255)
    picture = models.CharField(max_length=255, verbose_name="URL картинки")
    param = models.TextField(null=True)
    flavour = models.CharField(null = True,max_length=255, verbose_name="Вибір смаку")
    hqd_flavour = models.CharField(default="-", max_length=255)
    ukrainian_flavour = models.CharField(default="-",max_length = 255)
    disposable_flavour = models.CharField(default="-", max_length = 255)
    liquids_flavour = models.CharField(default="-", max_length=255)
    elf_bar_flavour = models.CharField(default="-", max_length=255)
    nicotine_strength = models.CharField(null = True,max_length=255, verbose_name="Міцність нікотину")
    fluid_volume = models.CharField(null = True,max_length=255, verbose_name="Обсяг рідини")
    battery_capacity = models.CharField(null = True,max_length=255, verbose_name="Ємність акумулятора")
    cartridge_capacity = models.CharField(null = True,max_length=255, verbose_name="Об'єм картриджа")
    resistance = models.CharField(null = True,max_length=255, verbose_name="Вибір опору")
    power = models.CharField(null = True,max_length = 255, verbose_name="Потужність")
    atomizer_volume = models.CharField(null = True,max_length=255, verbose_name="Обсяг атомайзера")
    max_power = models.CharField(null = True,max_length=255, verbose_name="Максимальна потужність")
    puffs_number = models.CharField(null = True,max_length=255, verbose_name="Кількість затяжок")
    rechargeable = models.BooleanField(null = True, verbose_name="Перезаряджаються'")
    compatibility_selection = models.CharField(null = True,max_length=255, verbose_name="Вибір сумісності")
    subscribers = models.TextField(null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Електронна цигарка"
        verbose_name_plural = "Електронні цигарки"
        ordering = ['categoryId', 'name']
    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_id': self.pk})


# class Parameters(models.Model):
#     id = models.ForeignKey(Podik, on_delete = models.CASCADE, primary_key=True)
    



# Create your models here.
class Areas_and_costs(models.Model):
    area = models.CharField(max_length=255, verbose_name="Область")
    cost_for_warehouse = models.IntegerField(default=0,verbose_name="Ціна за доставку у відділення")
    cost_for_post = models.IntegerField(default=0,verbose_name="Ціна за доставку у поштомат")
    cost_for_adress = models.IntegerField(default=0, verbose_name = "Ціна за доставку за адресою")
    class Meta:
        verbose_name = "Ціна за доставку"
        verbose_name_plural = "Ціни за доставку"
    
class NovaPost(models.Model):
    city = models.CharField(max_length=255)
    ref = models.CharField(max_length=37, primary_key=True)
    warehouses = models.TextField()
    mailboxes = models.TextField(null = True)
    area = models.CharField(max_length=255)
    isAreaCenter = models.BooleanField(default=False)

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    fee=models.IntegerField(verbose_name="Відсоток коміссії", validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ], default=5)
    class Meta:
        verbose_name = "Спосіб оплати"
        verbose_name_plural = "Способи оплати"

class Offers(models.Model):
    username = models.CharField(max_length=255, verbose_name="Ім'я користувача")
    offer = models.TextField(verbose_name="Замовлення")
    amount = models.CharField(max_length=255, verbose_name="Ціна")
    name = models.CharField(max_length=255, verbose_name="ПІБ")
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефону")
    call = models.BooleanField(null=True, verbose_name="Дзвонити")
    area = models.CharField(max_length=255, verbose_name="Область")
    city = models.CharField(max_length=255, verbose_name="Місто")
    warehouse = models.CharField(max_length=255, verbose_name="Пункт видачі")
    delivery_method = models.CharField(max_length=255,null=True, verbose_name="Спосіб доставки")
    payment_method = models.CharField(max_length=255,null=True, verbose_name="Спосіб оплати")
    comment = models.TextField(null=True, verbose_name="Коментар")
    products = models.TextField(null = True)
    offer_id = models.CharField(max_length=255,null=True, verbose_name="Id замовлення")
    tg_id = models.CharField(max_length=255, null=True)
    novapost_en = models.CharField(max_length=255, null=True,verbose_name="ТТН")
    status = models.CharField(max_length=255, null=True)
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

class CashbackPercentage(models.Model):
    percentage=models.IntegerField(verbose_name="Процент кешбека", validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ], default=5)
    class Meta:
        verbose_name = "Процент кешбека"
        verbose_name_plural = "Процент кешбека"
    def save(self, *args, **kwargs):
        if not self.pk and CashbackPercentage.objects.exists():
            raise ValidationError('There can only be one instance of this model.')
        return super(CashbackPercentage, self).save(*args, **kwargs)

class Users(models.Model):
    username = models.CharField(max_length=255, verbose_name="Ім'я користувача")
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефону")
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    tg_id = models.CharField(max_length=255, null = True, verbose_name="Id користувача")
    referral_count = models.IntegerField(null=True, verbose_name = "Кількість рефералів")
    message_text = models.CharField(max_length=255, null=True, verbose_name="Надіслати повідомлення")
    cashback_amount = models.IntegerField(verbose_name="Кешбек", default=0)
    class Meta:
        verbose_name = "Користувач бота"
        verbose_name_plural = "Користувачі бота"

class Filters(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва фільтру")
    visible = models.BooleanField(null = True, default = True, verbose_name="Доступність")
    class Meta:
        verbose_name = "Фільтр"
        verbose_name_plural = "Фільтри"