import os
import django

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE","pods.settings")
django.setup()

import requests
from main.models import Podik, Offers
import json

def to_sales_drive():
    offers = Offers.objects.all()
    offer = offers[len(offers)-1]
    products = []
    for product in offer.products.split(';'):
        print(product)
        if product.split(":")[0] != "":
            products.append(
                {"id": product.split(":")[0], "name": product.split(":")[1], "costPerItem": product.split(":")[2], "amount" : product.split(":")[3]},
                )
    print(products)
    if len(offer.name.split(' '))>1:
        s = ("Ні" if offer.call == False else "Так" )
        response = requests.post('https://podik228.salesdrive.me/handler/', json={
            "form": "WJB1FumGe-_rNRrqWrO4dnWi75PGNUkbUYeyxOKbAGhwXAJEA-Cb0YD7XExnRjA3YURIeW0oH2IDwmKL",
            "getResultData": "",
            "products": products,
            "fName": offer.name.split(' ')[1],
            "lName": offer.name.split(' ')[0],
            "phone": offer.phone_number,
            "payment_method": offer.payment_method,
            "shipping_method": offer.delivery_method,
            "shipping_address": offer.warehouse,
            "comment": offer.comment,
            "sajt": "Bot",
            "tgid":offer.tg_id,
            "zvonit":s,
            "orderid": offer.id,
            "novaposhta":{
                "area": offer.area,
                "city": offer.city,
                "WarehouseNumber": offer.warehouse,
            }
            })
    else:
        s = ("Ні" if offer.call == False else "Так" )
        response = requests.post('https://podik228.salesdrive.me/handler/', json={
            "form": "WJB1FumGe-_rNRrqWrO4dnWi75PGNUkbUYeyxOKbAGhwXAJEA-Cb0YD7XExnRjA3YURIeW0oH2IDwmKL",
            "getResultData": "",
            "products": products,
            "fName": offer.name,
            "phone": offer.phone_number,
            "payment_method": offer.payment_method,
            "shipping_method": offer.delivery_method,
            "shipping_address": offer.warehouse,
            "comment": offer.comment,
            "sajt": "Bot",
            "tgid": offer.tg_id,
            "zvonit": s,
            "orderid": offer.id,
            "novaposhta":{
                "area": offer.area,
                "city": offer.city,
                "WarehouseNumber": offer.warehouse,
            }
            })
    print(response.text)

# to_sales_drive()