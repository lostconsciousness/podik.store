# import requests

# url = 'https://api.novaposhta.ua/v2.0/json/'
# api_key = '9fca35c6a673642fc96b4bbccc542ad3'
# method = 'Address.getSettlements'
# params = {
#     'apiKey': api_key,
#     'modelName': 'Address',
#     'calledMethod': method,
# }

# response = requests.get(url, json=params)

# result = response.text
# for city in result:
#     print(city['Description'])
# print(result['data'])

# # cities = result['data']
# # for city in cities:
# #     print(city['Description'])
import requests
import json
bool = False
url = 'https://api.novaposhta.ua/v2.0/json/'
api_key = '9fca35c6a673642fc96b4bbccc542ad3'
method = 'getCities'
params = {
    'apiKey': api_key,
    'modelName': 'Address',
    'calledMethod': 'getAreas',
}
areas_centers = []

response = requests.post(url, json=params)
result = response.json()
i = 0
if 'data' in result:
    areas = result['data']
    for area in areas:
        areas_centers.append(area['AreasCenter'])
        print(areas_centers[i])
        i = i + 1
else:
    print(result['errors'])

areas_centers_names = []

url = 'https://api.novaposhta.ua/v2.0/json/'
api_key = '9fca35c6a673642fc96b4bbccc542ad3'
method = 'getCities'
params = {
    'apiKey': api_key,
    'modelName': 'Address',
    'calledMethod': 'getCities',
    "methodProperties": {
        "Page" : f"{0}"
}
}

response = requests.post(url, json=params)
result = response.json()

if 'data' in result:
    areas = result['data']
    for area in areas:
        if area['Ref'] in areas_centers:
            areas_centers_names.append(area['Description'])
            
else:
    print(result['errors'])

s = "Усі обласні центри України:"
for city in areas_centers_names:
    s = s+f"\n{city}"
print(s)

def find_warehouse(city_name):
    url = 'https://api.novaposhta.ua/v2.0/json/'
    api_key = '9fca35c6a673642fc96b4bbccc542ad3'
    params = {
        'apiKey': api_key,
        'modelName': 'Address',
        'calledMethod': 'getWarehouses',
        "methodProperties": {
            "CityName": city_name,
            "Page" : f"{0}"
        }
    }
    
    params2 = {
    "apiKey": api_key,
    "modelName": "Address",
    "calledMethod": "getWarehouseTypes",
    }
    response = requests.post(url, json=params)
    result = response.json()
    ans = []
    response2 = requests.post(url, json=params2)
    result2 = response2.json()
    types = result2['data']
    a = []
    iter = 0
    for i in types:
        #  if iter == 10:
        #         break
        #  iter= iter+1
         if i['Description'] == "Поштове відділення":
            a.append(i['Ref'])
            print( i['Ref'])
    if 'data' in result:
        iter = 0
        areas = result['data']
        for area in areas:
            # if iter == 10:
            #     break
            # iter= iter+1
            if area['TypeOfWarehouse'] in a: 
                ans.append(area['Description'])
                print(area['Description'])
            
    else:
        print(result['errors'])
    return ans