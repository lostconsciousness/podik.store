import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE","pods.settings")
django.setup()

from main.models import Podik, Filters
import xmltodict
import json
from bs4 import BeautifulSoup
from django.db import transaction
import time
import requests
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions
import asyncio

bot = Bot(token="6075679825:AAGrgD6b9hybk9EoNue44k1ZPW8paFJCs5M")
dp = Dispatcher(bot)


async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

def unloading():
    response = requests.get(
        "https://anix.salesdrive.me/export/yml/export.yml?publicKey=fl6yiRQy6G170JBBaa7eFQehljUhWWgNxHpuiPpH03IgQWVb5z98Jw6SBhIj"
    )
    with open("media/final.xml", "w+", encoding="utf-8") as file:
        file.write(response.text)

    # Преобразование данных в формат JSON
    json_data = json.dumps(xmltodict.parse(response.text), indent=4)

    # Сохранение данных в файле JSON
    with open('data.json', 'w') as f:
        f.write(json_data)

class DBManager:
    def __str_to_bool(self,s):
        return s.lower() in ['true', '1', 't', 'y', 'yes']
    

    # def addToDB(self):
    #     data = json.load(open("alldata.json", "r", encoding="UTF-8"))
    #     Podik.objects.all().delete()
    #     pods = data["yml_catalog"]["shop"][0]["offers"][0]["offer"]
        
    #     # print(pods[0]["$"])
    #     # print(self.__str_to_bool("false"))
    #     j = 0
    #     print(len(pods))
    #     for pod in pods:
    #         j = j + 1
    #         if j == 5383:
    #             break
    #         print(j)
    #         picture = '-'
    #         try:
    #             picture=pod["picture"][0]
    #         except:
    #             picture="-"
    #         par = ""
    #         try:
    #             for parametr in pod['param']:
    #                 par =par + parametr["$"]["name"] + " = " + parametr["_"]+", "
    #         except:
    #             par = "-"
    #         flavour = '-'
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Выбор вкуса":
    #                     flavour=parametr["_"]
    #         except:
    #             flavour="-"
    #         nicotine_strength = '-'
    #         try:
    #             nicotine_strength = ''
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Крепость никотина" or parametr["$"]["name"] == "Выбор крепости":
    #                     for i in parametr["_"]:
    #                         if i.isdigit():
    #                             nicotine_strength = nicotine_strength+i
    #         except:
    #             nicotine_strength="-"
    #         nicotine_type = '-'
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Вид никотина":
    #                     nicotine_type = parametr["_"]
    #         except:
    #             nicotine_type="-"
    #         fluid_volume = '-'
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Объем жидкости":
    #                     fluid_volume = parametr["_"]
    #         except:
    #             fluid_volume="-"
    #         battery_capacity = '-'
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Ёмкость аккумулятора":
    #                     for i in parametr["_"].split(" "):
    #                         if i.isdigit():
    #                             battery_capacity = str(i) + " mAh"
    #         except:
    #             battery_capacity="-"
    #         cartridge_capacity = "-"
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Объём картриджа":
    #                     cartridge_capacity = parametr["_"]
    #         except:
    #             cartridge_capacity="-"

    #         resistance = '-'
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Выбор сопротивления":
    #                     resistance = parametr["_"]
    #         except:
    #             resistance="-"

    #         power = ""
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Мощность":
    #                     power = parametr["_"]
    #         except:
    #             power="-"
    #         atomizer_volume = "-"
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Объем атомайзера":
    #                     if parametr["_"][-1] != ".":
    #                         atomizer_volume = parametr["_"] + "."
    #                     else:
    #                         atomizer_volume = parametr["_"]
    #         except:
    #             atomizer_volume="-"

    #         max_power = "-"
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Максимальная мощность":
    #                     for i in parametr["_"].split(" "):
    #                         if i.isdigit():
    #                             max_power = str(i) + " Вт"
    #         except:
    #             max_power="-"

    #         puffs_number = "-"
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Количество затяжек" or parametr["$"]["name"] == "Выбор количества затяжек":
    #                     puffs_number = parametr["_"]
    #         except:
    #             puffs_number="-"

    #         rechargeable = None
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Перезаряжаемые":
    #                     if parametr["_"] == "Так":
    #                         rechargeable = True
    #                     else:
    #                         rechargeable = False
    #         except:
    #             rechargeable=None

    #         compatibility_selection = "-"
    #         try:
    #             for parametr in pod['param']:
    #                 if parametr["$"]["name"] == "Выбор совместимости":
    #                     compatibility_selection = parametr["_"]
    #         except:
    #             compatibility_selection="-"
    #         print(pod["name"][0])
    #         podik = Podik(
    #             id = pod["$"]["id"],
    #             available = self.__str_to_bool(pod["$"]["available"]),
    #             price = int(pod["price"][0]),
    #             currencyId =pod["currencyId"][0],
    #             name=pod["name"][0],
    #             categoryId=int(pod["categoryId"][0]),
    #             vendorCode=int(pod["vendorCode"][0]),
    #             # description=pod["description"][0],
    #             quantity_in_stock=int(pod["quantity_in_stock"][0]),
    #             url=pod["url"][0],
    #             picture=picture,
    #             param=par,
    #             flavour = flavour,
    #             nicotine_strength = nicotine_strength[:2],
    #             fluid_volume = fluid_volume,
    #             battery_capacity = battery_capacity,
    #             cartridge_capacity = cartridge_capacity,
    #             resistance = resistance,
    #             power = power,
    #             atomizer_volume = atomizer_volume,
    #             max_power = max_power,
    #             puffs_number = puffs_number,
    #             rechargeable = rechargeable,
    #             compatibility_selection = compatibility_selection,
    #         )
    #         podik.save()
    #     exit()
    def check(self):
        data = json.load(open("data.json", "r", encoding="UTF-8"))
        pods = data["yml_catalog"]["shop"]["offers"]["offer"]
        id_povtorenia = []
        params = []
        for pod in pods:
            try:
                params = pod["param"]
                for param in params:
                    if pod["categoryId"]+": "+ param['@name'] not in id_povtorenia:
                        id_povtorenia.append(pod["categoryId"]+": "+ param['@name'])
            except:
                pass
                
        print(id_povtorenia)
    def addXmlToDB(self):
        with open('offer.xml', 'r',encoding='utf-8') as f:
            data = f.read()
        bs_data = BeautifulSoup(data, "xml")
        pods = bs_data.find_all('offer')
        for pod in pods:
            podik = Podik(
                id = pod['id'],
                available = self.__str_to_bool(pod["available"]),
                price = int(pod.find('price').text),
                currencyId = pod.find('currencyId').text,
                name = pod.find('name').text,
                categoryId=int(pod.find('categoryId').text),
                vendorCode=int(pod.find('vendorCode').text),
                # description=pod.find('description').text,
                quantity_in_stock=int(pod.find('quantity_in_stock').text),
                url=pod.find('url').text,
                picture=pod.find('picture').text,
                #params=pod["param"][0]["_"],
            )
            podik.save()
       
    def JsonToDB(self):
        data = json.load(open("data.json", "r", encoding="UTF-8"))

        subscribed_users = {}
        pods_unavailable = list(Podik.objects.filter(available=False))
        for pod in pods_unavailable:
            subscribed_users[pod.id] = pod.subscribers

        Podik.objects.all().delete()
        pods = data["yml_catalog"]["shop"]["offers"]["offer"]
        all_pods = []
        j = 0
        for pod in pods:
            j = j + 1
            # print(j)
            picture = '-'
            try:
                picture=(pod["picture"] if len(pod["picture"][0])==1 else pod["picture"][0])
                # print(picture)
            except:
                picture="-"
            par = ""
            try:
                for parametr in pod['param']:
                    par =par + parametr["@name"] + " = " + parametr["#text"]+", "
            except:
                par = "-"
            flavour = '-'
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор вкуса":
                        flavour=parametr["#text"]
            except:
                flavour="-"
            nicotine_strength = '-'
            try:
                nicotine_strength = ''
                for parametr in pod['param']:
                    if parametr["@name"] == "Крепость никотина" or parametr["@name"] == "Выбор крепости":
                        for i in parametr["#text"]:
                            if i.isdigit():
                                nicotine_strength = nicotine_strength+i
            except:
                nicotine_strength="-"
            nicotine_type = '-'
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Вид никотина":
                        nicotine_type = parametr["#text"]
            except:
                nicotine_type="-"
            fluid_volume = '-'
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Объем жидкости":
                        fluid_volume = parametr["#text"]
            except:
                fluid_volume="-"
            battery_capacity = '-'
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Ёмкость аккумулятора":
                        for i in parametr["#text"].split(" "):
                            if i.isdigit():
                                battery_capacity = str(i) + " mAh"
            except:
                battery_capacity="-"
            cartridge_capacity = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Объём картриджа":
                        cartridge_capacity = parametr["#text"]
            except:
                cartridge_capacity="-"

            resistance = '-'
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор сопротивления":
                        resistance = parametr["#text"]
            except:
                resistance="-"

            power = ""
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Мощность":
                        power = parametr["#text"]
            except:
                power="-"
            atomizer_volume = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Объем атомайзера":
                        if parametr["#text"][-1] != ".":
                            atomizer_volume = parametr["#text"] + "."
                        else:
                            atomizer_volume = parametr["#text"]
            except:
                atomizer_volume="-"

            max_power = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Максимальная мощность":
                        for i in parametr["#text"].split(" "):
                            if i.isdigit():
                                max_power = str(i) + " Вт"
            except:
                max_power="-"

            puffs_number = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Количество затяжек" or parametr["@name"] == "Выбор количества затяжек":
                        puffs_number = parametr["#text"]
            except:
                puffs_number="-"

            rechargeable = None
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Перезаряжаемые":
                        if parametr["#text"] == "Так":
                            rechargeable = True
                        else:
                            rechargeable = False
            except:
                rechargeable=None

            compatibility_selection = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор совместимости":
                        compatibility_selection = parametr["#text"]
            except:
                compatibility_selection="-"
            # print(pod["price"])

            subscribe = None
            if pod['@id'] in list(subscribed_users.keys()) and self.__str_to_bool(pod["@available"]):
                print('notification')
                if subscribed_users[pod['@id']] != None:
                    for user in subscribed_users[pod['@id']].split(';')[:-1]:
                        print(user)
                        asyncio.run(send_message(user, f"{pod['name']} з'явився у наявності"))
                        
            elif pod['@id'] in list(subscribed_users.keys()) and not self.__str_to_bool(pod["@available"]):
                if subscribed_users[pod['@id']] != None:
                    subscribe = subscribed_users[pod['@id']]

            disposable_flavour = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор вкуса" and pod['categoryId'] == "239":
                        disposable_flavour=parametr["#text"]
            except:
                disposable_flavour="-"

            elf_bar_flavour = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор вкуса" and pod['categoryId'] == "287":
                        elf_bar_flavour=parametr["#text"]
            except:
                elf_bar_flavour="-"

            ukrainian_flavour = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор вкуса" and pod['categoryId'] == "236":
                        ukrainian_flavour=parametr["#text"]
            except:
                ukrainian_flavour="-"

            liquids_flavour = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор вкуса" and pod['categoryId'] == "208":
                        liquids_flavour=parametr["#text"]
            except:
                liquids_flavour="-"

            hqd_flavour = "-"
            try:
                for parametr in pod['param']:
                    if parametr["@name"] == "Выбор вкуса" and pod['categoryId'] == "288":
                        hqd_flavour=parametr["#text"]
            except:
                hqd_flavour="-"
            podik = Podik(
                id = pod["@id"],
                available = self.__str_to_bool(pod["@available"]),
                price = int(round(float(pod['price']))),
                currencyId =pod["currencyId"],
                name=pod["name"],
                categoryId=int(pod["categoryId"]),
                vendorCode=pod["vendorCode"].replace("GIFTCARD","0"),
                # description=pod["description"][0],
                quantity_in_stock=int(pod["quantity_in_stock"]),
                url=pod["url"],
                picture=picture,
                param=par,
                flavour = flavour,
                nicotine_strength = nicotine_strength[:2],
                fluid_volume = fluid_volume,
                battery_capacity = battery_capacity,
                cartridge_capacity = cartridge_capacity,
                resistance = resistance,
                power = power,
                atomizer_volume = atomizer_volume,
                max_power = max_power,
                puffs_number = puffs_number,
                rechargeable = rechargeable,
                compatibility_selection = compatibility_selection,
                subscribers = subscribe,
                disposable_flavour = disposable_flavour,
                elf_bar_flavour = elf_bar_flavour,
                hqd_flavour = hqd_flavour,
                liquids_flavour = liquids_flavour,
                ukrainian_flavour = ukrainian_flavour,
            )
            # print("hihi="+str(int(pod["categoryId"])))
            all_pods.append(podik)
        Podik.objects.bulk_create(all_pods)
        # print(len(pods))
        # print('finish')


def all_categories():
    # Filters.objects.all().delete()
    # Filters(name = "Перезаряджаються", visible = 1).save()
    # Filters(name = "Кількість затяжок", visible = 1).save()
    # Filters(name = "Максимальна потужність", visible = 1).save()
    # Filters(name = "Обсяг атомайзера", visible = 1).save()
    # Filters(name = "Потужність", visible = 1).save()
    # Filters(name = "Вибір опору", visible = 1).save()
    # Filters(name = "Об'єм картриджа", visible = 1).save()
    # Filters(name = "Ємність акумулятора", visible = 1).save()
    # Filters(name = "Обсяг рідини", visible = 1).save()
    # Filters(name = "Міцність нікотину", visible = 1).save()

    data = json.load(open("data.json", "r", encoding="UTF-8"))
    categories = data["yml_catalog"]["shop"]["categories"]['category']
    real_all_cats = []
    for category in categories:
        all_cats = []
        all_cats.append(category['@id'])
        all_cats.append(category['#text'])
        real_all_cats.append(tuple(all_cats))
    return tuple(real_all_cats)

# print(all_categories())
dbm = DBManager()
# dbm.JsonToDB()

# dbm.check()

unloading()
dbm.JsonToDB()

# while(True):
#     unloading()
#     dbm.JsonToDB()
#     time.sleep(30)

# dbm.addXmlToDB()