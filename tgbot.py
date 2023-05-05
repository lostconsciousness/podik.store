import os
import django

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE","pods.settings")
django.setup()

from aiogram import executor, Bot, Dispatcher, types
from aiogram.utils.deep_linking import get_start_link
from newpost import areas_centers_names, find_warehouse
import requests
import json
import string
import random
from main.models import Offers, Users, Areas_and_costs
from test import to_sales_drive
import barcode
from barcode.writer import ImageWriter
import io
from django.db.models.signals import post_save
from django.dispatch import receiver

token = "6075679825:AAGrgD6b9hybk9EoNue44k1ZPW8paFJCs5M"

telegram_id = []

bot = Bot(token)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def start_fun(message: types.Message):
    Users.objects.all()
    existing_user = Users.objects.filter(username=message.from_user.username).first()
    if len(message.text.split())!=1:
        if not existing_user:
            referral_id = message.text.split()[1]
            Users.objects.all().filter(tg_id=referral_id).update(referral_count = int(Users.objects.all().filter(tg_id=referral_id)[0].referral_count)+1)
            await bot.send_message(message.from_user.id,"Ви під'єднались за реферальним кодом!")
            await bot.send_message(referral_id, "За вашим реферальним кодом під'єднався користувач!")
    print(message.from_user.username+": "+ message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kbbutton1 = types.KeyboardButton(text = "Так, мені є 18 років.")
    kbbutton2 = types.KeyboardButton(text = "Ні, мені ще немає 18 років.")
    keyboard.add(kbbutton1, kbbutton2)
    await message.answer('Вас вітає бот з продажу електронних сигарет! Чи є вам 18 років? ', reply_markup=keyboard) 

@dp.message_handler(lambda message: message.text == "Повернутися на минулий крок.")
async def startagain(message:types.Message):
    print(message.from_user.username+": "+ message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kbbutton1 = types.KeyboardButton(text = "Так, мені є 18 років.")
    kbbutton2 = types.KeyboardButton(text = "Ні, мені ще немає 18 років.")
    keyboard.add(kbbutton1, kbbutton2)
    await message.answer('Вас вітає бот з продажу електронних сигарет! Чи є вам 18 років? ', reply_markup=keyboard) 

@dp.message_handler(lambda message: message.text == "Ні, мені ще немає 18 років.")
async def no18(message:types.Message):
    print(message.from_user.username+": "+ message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kbbutton1 = types.KeyboardButton(text = "Повернутися на минулий крок.")
    keyboard.add(kbbutton1)
    await message.answer('Продаж нашої продукції дозволений лише людям що досягли повноліття.', reply_markup=keyboard) 

@dp.message_handler(lambda message: message.text == 'Так, мені є 18 років.') 
async def start_fun(message: types.Message):
    print(message.from_user.username+": "+ message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kbbutton1 = types.KeyboardButton(text = "Поділитися номером телефону.", request_contact=True)
    keyboard.add(kbbutton1)
    await message.answer('Надішліть, будь ласка, свій номер телефону: ', reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def qq(message:types.Message):
    Users.objects.all()
    existing_user = Users.objects.filter(username=message.from_user.username).first()
    if not existing_user:
        user = Users(
            username=message.from_user.username,
            phone_number=message.contact.phone_number,
            name=message.from_user.first_name,
            tg_id = message.from_id,
            referral_count = 0,
        )
        user.save()
    print(message.from_user.username+": "+ message.contact.phone_number)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text = "Site", web_app = types.WebAppInfo(url=f"https://general2286.pythonanywhere.com/{message.from_id}"))],
            [types.KeyboardButton(text = "Запросити друга"), types.KeyboardButton(text = "Звʼяжіться з нами")],
            [types.KeyboardButton(text = "Картка користувача"), types.KeyboardButton(text = "Знайти найближчий магазин")],
            [types.KeyboardButton(text = "Мої замовлення")],
        ],
        resize_keyboard=True
    )
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.row(
        types.InlineKeyboardButton(
            text="Перейти до магазину",
            web_app=types.WebAppInfo(url=f"https://general2286.pythonanywhere.com/{message.from_id}"),
        )
    )
    await bot.send_message(
        message.from_user.id,
        "Натисніть кнопку 'Перейти до магазину' та відкриється наш інтернет-магазин.",
        reply_markup=keyboard,
    )

@dp.message_handler(lambda message: message.text == "Звʼяжіться з нами")
async def my_orders(message: types.Message):
    print(message.from_user.username+": "+ message.text)
    await bot.send_message(message.from_user.id, """💬 Онлайн-чат:

Telegram - https://t.me/UVAPE_SUPPORT_bot
Viber - https://tinyurl.com/y4ur6pw8

📞 Зв’яжіться з нами по телефонам:

+38 (093) 323 7887
+38 (096) 323 7887
+38 (099) 323 7887""")
    
@dp.message_handler(lambda message: message.text == "Знайти найближчий магазин")
async def my_orders(message: types.Message):
    print(message.from_user.username+": "+ message.text)
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.row(
        types.InlineKeyboardButton(
            text="Найближчий магазин",
            web_app=types.WebAppInfo(url="https://uvape.pro/contact-us#adrshop"),
        )
    )
    await bot.send_message(message.from_id,text="Найближчий магазин Ви можете знайти за посиланням:", reply_markup=reply_markup) 

@dp.message_handler(lambda message: message.text == "Мої замовлення")
async def my_orders(message: types.Message):
    print(message.from_user.username+": "+ message.text)
    offers = Offers.objects.all().filter(tg_id = message.from_id)
    order_str=""
    i = 1
    for order in offers:
        try:
            order_str+=f"\n{i})Заказ {order.id}"+"\n"+order.offer+f"Сумма заказа: {order.amount}\nСтатус заказа:\nТТН: "+order.novapost_en
        except:
            order_str+=f"\n{i})Заказ {order.id}"+"\n"+order.offer+f"Сумма заказа: {order.amount}\nСтатус заказа:"
        i = i + 1
    await bot.send_message(message.from_user.id, "Мои заказы:"+order_str)

@dp.message_handler(lambda message: message.text == "Картка користувача")
async def client_card(message: types.Message):
    print(message.from_user.username+": "+ message.text)
    # code = "yourcardnumber"
    code = str(message.from_user.id)
    buf = io.BytesIO()
    code_bar=barcode.Code39(code, writer=ImageWriter(), add_checksum=False)
    code_bar.write(buf)
    buf.seek(0)
    await bot.send_photo(message.from_user.id, buf, f"Ваша бонусная карта\nВаш кешбек: {get_cashback(message.from_user.id)}")

@dp.message_handler(lambda message: message.text == "Запросити друга")
async def invite(message:types.Message):
    print(message.from_user.username+": "+ message.text)
    await bot.send_message(message.from_user.id,f"Запросіть друга за посиланням: ", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Поделится", url=f"https://t.me/share/url?url=https://t.me/ecigtestbot?start={message.from_user.id}")))



@dp.message_handler(commands = ['pay'])
async def payment(message:types.Message):
    #print(message.from_user.username+": "+ message.contact.phone_number)
    print(int(message.text.split(" ")[1]))
    w4purl = "https://api.wayforpay.com/api"
    allObjects = ['Одноразовая электронная сигарета Airis Lux P5000 Pina Colada', 'Одноразовая электронная сигарета R&M Legend 10000 затяжек Big Bang Fruit', 'Одноразовая сигарета Joyetech VAAL MAX Lush Ice', 'Одноразовая сигарета Joyetech VAAL GLAZ6500 Passion Fruit Orange Guava', 'Одноразовая сигарета Joyetech VAAL EP4500 Cotton Candy', 'Одноразовая сигарета Joyetech VAAL EP4500 Peach Mango Watermelon', 'Одноразовая электронная сигарета Elf Bar BC3500 3500 затяжек Cranberry Grape', 'Chaser Salt for Pods 15 мл 50 мг (5.0%) Bali Triple Shot', 'Chaser Salt - Blackcurrant Menthol (Черная смородина с ментолом) 10мл 30 мг (3.0%)', '3Ger Salt 15 мл 35 мг (3,5%) Apple Caramel']
    random_elements = random.sample(allObjects, 5)
    new=[]
    for i in random_elements:
        i = i.replace("%", "")
        new.append(i)
    print(new)
    j = ""
    with open('txt.txt', 'r', encoding ='utf-8') as f:
        j = f.readline()
    data = {
    "transactionType":"CREATE_INVOICE",
    "merchantAccount":"test_merch_n1",
    "merchantAuthType":"SimpleSignature",
    "merchantDomainName":"www.market.ua",
    # "merchantSignature":"60c5d743b71f79abe48c7183ada4b451",
    "apiVersion":1,
    "language":"ru",
    "serviceUrl":"https://eovbu9r2zfhhsp8.m.pipedream.net",
    "orderReference":"DH18799397" + str(j),
    "orderDate":1415379863,
    "amount":int(message.text.split(" ")[1]),
    "currency":"UAH",
    "orderTimeout": 60,
    "productName": new,
    "productPrice":[1000,547, 432, 234, 324],
    "productCount":[1,1, 1,1,1],
    "paymentSystems": "card;privat24",
    "clientFirstName":"Bulba",
    "clientLastName":"Taras",
    "clientEmail":"rob@mail.com",
    "clientPhone":"380556667788"
    }
    print(type(j))
    print(j)
    j= int(j)+1
    with open('txt.txt', 'w') as f:
        f.write(str(j))
    # response=requests.get(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string=test_merch_n1%3Bwww.market.ua%3BDH1679956997%3B1415379863%3B158%3BUAH%3B%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D1%80%20Intel%20Core%20i5-4670%203.4GHz%3B%D0%9F%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20Kingston%20DDR3-1600%204096MB%  productPrice   20PC3-12800%3B1%3B1%3B1000%3B547&key=flk3409refn54t54t*FNJRET')
    def create_signature(data:dict):
        print(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string={data["merchantAccount"]}%3B{data["merchantDomainName"]}%3B{data["orderReference"]}%3B{data["orderDate"]}%3B{data["amount"]}%3B{data["currency"]}%3B{"%3B".join(data["productName"])}%3B{"%3B".join(str(i) for i in data["productCount"])}%3B{"%3B".join(str(i) for i in data["productPrice"])}&key=flk3409refn54t54t*FNJRET')
        response=requests.get(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string={data["merchantAccount"]}%3B{data["merchantDomainName"]}%3B{data["orderReference"]}%3B{data["orderDate"]}%3B{data["amount"]}%3B{data["currency"]}%3B{"%3B".join(data["productName"])}%3B{"%3B".join(str(i) for i in data["productCount"])}%3B{"%3B".join(str(i) for i in data["productPrice"])}&key=flk3409refn54t54t*FNJRET')
        return response.text
    signature=create_signature(data)
    data["merchantSignature"]=signature
    print(w4purl)

    response = requests.post(w4purl, json.dumps(data))
    print(response.text)
    json_obj = json.loads(response.text)
    w4purl = json_obj["invoiceUrl"].replace("\\","")
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.row(
        types.InlineKeyboardButton(
            text="Сплатити",
            url=w4purl,
        )
    )
    await message.answer(text = "натисніть кнопку сплати", reply_markup=reply_markup)

import mysql.connector

config={
        "password": "Trnn06771588990",
        "host": "database-2.ctng339lkkzz.eu-north-1.rds.amazonaws.com",
        "user": "admin",
        "port":"3306",
        "database": "db",
        }


def get_cashback(tg_id):
    base = mysql.connector.connect(**config)
    cur = base.cursor()
    cur.execute("SELECT cashback_amount FROM main_users WHERE tg_id=%(tg_id)s",{"tg_id":tg_id})
    res= cur.fetchall()[0][0]
    return res

@dp.message_handler(content_types=types.ContentType.ANY)
async def spec(message:types.Message):
    print(message.from_id)
    try:
        j = ""
        with open('txt.txt', 'r', encoding ='utf-8') as f:
            j = f.readline()
        Offers.objects.all()
        user_info = json.loads(message.web_app_data.data)
        
        offer = Offers(
            username = message.from_user.username,
            offer = user_info['offer'],
            amount = str(int(user_info['amount'].split(' ')[0])),
            name = user_info['name'],
            phone_number = user_info['phone_number'].replace("(","").replace(")","").replace("-","").replace("+",""),
            call = user_info['call'],
            area = user_info['area'],
            city = user_info['city'],
            warehouse = user_info['warehouse'],
            products = user_info['products'],
            delivery_method = user_info['delivery_method'],
            comment = user_info['comment'],
            payment_method = user_info['payment_method'],
            offer_id = j,
            tg_id = message.from_id
                        )
        offer.save()

        to_sales_drive()
        print(offer.call)

        await message.answer(text ="Номер замовлення: "+str(offer.id)+"\n"+json.loads(message.web_app_data.data)['message'])
        await message.answer(text =str(int(user_info['amount'].split(' ')[0])))
        if user_info['payment_method'] == "Карткою онлайн":
            productName = []
            productName.append(user_info['products'].split('-')[0])
            w4purl = "https://api.wayforpay.com/api"
            j = ""
            with open('txt.txt', 'r', encoding ='utf-8') as f:
                j = f.readline()
            data = {
            "transactionType":"CREATE_INVOICE",
            "merchantAccount":"test_merch_n1",
            "merchantAuthType":"SimpleSignature",
            "merchantDomainName":"www.market.ua",
            # "merchantSignature":"60c5d743b71f79abe48c7183ada4b451",
            "apiVersion":1,
            "language":"ru",
            "serviceUrl":"https://eovbu9r2zfhhsp8.m.pipedream.net",
            "orderReference":"DH18799378" + str(j),
            "orderDate":1415379863,
            "amount": int(user_info['amount'].replace("UAH","")),
            "currency":"UAH",
            "orderTimeout": 60,
            "productName": productName,
            "productPrice":[1000],
            "productCount":[1],
            "paymentSystems": "card;privat24",
            "clientFirstName":"user_info['name']",
            "clientPhone":user_info['phone_number']
            }
            print(type(j))
            print(j)
            j= int(j)+1
            with open('txt.txt', 'w') as f:
                f.write(str(j))
            # response=requests.get(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string=test_merch_n1%3Bwww.market.ua%3BDH1679956997%3B1415379863%3B158%3BUAH%3B%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D1%80%20Intel%20Core%20i5-4670%203.4GHz%3B%D0%9F%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20Kingston%20DDR3-1600%204096MB%  productPrice   20PC3-12800%3B1%3B1%3B1000%3B547&key=flk3409refn54t54t*FNJRET')
            def create_signature(data:dict):
                print(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string={data["merchantAccount"]}%3B{data["merchantDomainName"]}%3B{data["orderReference"]}%3B{data["orderDate"]}%3B{data["amount"]}%3B{data["currency"]}%3B{"%3B".join(data["productName"])}%3B{"%3B".join(str(i) for i in data["productCount"])}%3B{"%3B".join(str(i) for i in data["productPrice"])}&key=flk3409refn54t54t*FNJRET')
                response=requests.get(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string={data["merchantAccount"]}%3B{data["merchantDomainName"]}%3B{data["orderReference"]}%3B{data["orderDate"]}%3B{data["amount"]}%3B{data["currency"]}%3B{"%3B".join(data["productName"])}%3B{"%3B".join(str(i) for i in data["productCount"])}%3B{"%3B".join(str(i) for i in data["productPrice"])}&key=flk3409refn54t54t*FNJRET')
                return response.text
            signature=create_signature(data)
            data["merchantSignature"]=signature
            print(w4purl)

            response = requests.post(w4purl, json.dumps(data))
            print(response.text)
            json_obj = json.loads(response.text)
            w4purl = json_obj["invoiceUrl"].replace("\\","")
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.row(
                types.InlineKeyboardButton(
                    text="Сплатити",
                    url=w4purl,
                )
            )
            await message.answer(text = "натисніть кнопку сплати", reply_markup=reply_markup)
            j = int(j)+1
            with open('txt.txt', 'w') as f:
                f.write(str(j))
    except:
        print("sosunok")
        print(message.from_user.username+": "+ message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
