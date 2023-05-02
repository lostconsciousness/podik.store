import requests
import json
import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE","pods.settings")
django.setup()

from main.models import NovaPost, Areas_and_costs



URL = 'https://api.novaposhta.ua/v2.0/json/'
API_KEY = '9fca35c6a673642fc96b4bbccc542ad3'

def get_areas():
   all_areas = []
   areas_centers=[]
   params = {
      "apiKey": API_KEY,
      "modelName": "Address",
      "calledMethod": "getAreas",
      "methodProperties": {   }
   }

   response = requests.post(URL, json=params)
   result = response.json()

   i = 0
   if 'data' in result:
      areas = result['data']
      for area in areas:
         areas_centers.append(area['AreasCenter'])
         # area_and_cost = Areas_and_costs(
         #    area = area['Description'],
         # )
         # all_areas.append(area_and_cost)
         i = i + 1
   else:
      print(result['errors'])
   # Areas_and_costs.objects.bulk_create(all_areas)
   return areas_centers

def get_areas_centers():
   areas_centers = get_areas()
   areas_centers_names = []

   params = {
      'apiKey': API_KEY,
      'modelName': 'Address',
      'calledMethod': 'getCities',
      "methodProperties": {
         "Page" : f"{0}"
      }
   }

   response = requests.post(URL, json=params)
   result = response.json()

   if 'data' in result:
      areas = result['data']
      for area in areas:
         if area['Ref'] in areas_centers:
               areas_centers_names.append(area['Description'])
               
   else:
      print(result['errors'])

   return areas_centers_names

def get_cities_and_add_to_db():
   NovaPost.objects.all().delete()
   all_nova_post = []
   area_centers = get_areas_centers()
   print(area_centers)

   i = 0
   while True:
      city = {}
      params = {
         "apiKey": API_KEY,
         "modelName": "Address",
         "calledMethod": "getSettlements",
         "methodProperties": {
         "Page":f"{i}"
         }
      }

      response = requests.post(URL, json=params)
      result = response.json()
      all_np_data = []
      if 'data' in result:
         if len(result['data']) == 0:
            break
         cities_ = result['data']
         for city_ in cities_:
            if city_['SettlementTypeDescription'] != 'місто':
               continue
            warehouses = get_warehouses(city_['Ref'])
            if warehouses == '':
               continue
            wh = warehouses[0] + ";"+ warehouses[1]
            novapost = NovaPost(city=city_['Description'], ref=city_['Ref'], area=city_['AreaDescription'], warehouses=warehouses[0], mailboxes = warehouses[1], isAreaCenter=(True if city_['Description'] in area_centers else False))
            #all_np_data.append(novapost)
            novapost.save()
            all_nova_post.append(novapost)
            print(city_['Description'])
      i+=1
   return all_nova_post
      

def get_warehouses(ref):
   i = 1
   warehouses = ['','']
   while True:
      params = {
      "apiKey": API_KEY,
      "modelName": "Address",
      "calledMethod": "getWarehouses",
      "methodProperties": {
         "SettlementRef": ref,
         "Page" : f"{i}",
         }
      }
      response = requests.post(URL, json=params)
      result = response.json()
      if 'data' in result:
         if len(result['data']) == 0:
            break
         warehouses_ = result['data']
         for house in warehouses_:
            if 'Поштомат' not in house['Description']:
               warehouses[0] += house['Description'].replace('`', '').replace("'", '').replace('\'', '').replace('"', '') + ';'
            else:
               warehouses[1] += house['Description'].replace('`', '').replace("'", '').replace('\'', '').replace('"', '') + ';'
         i+=1
   print(warehouses)
   return warehouses

get_cities_and_add_to_db()

# while(True):
#    print(get_cities_and_add_to_db())
#    time.sleep(60)
# print(get_areas_centers())