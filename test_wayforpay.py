import requests
import json
import string
import random


# Указываем URL API WayForPay
url = "https://api.wayforpay.com/api"

# Задаем параметры платежа
# data = {
#     "transactionType": "CREATE_INVOICE",
#     "merchantAccount": "test_merch_n1",

#     "secretKey":"flk3409refn54t54t*FNJRET",
#     "merchantDomainName": "www.market.com",
#     # "orderReference": "YOUR_ORDER_REFERENCE",
#     "apiVersion":"1",
#     "amount": "10",
#     "merchantSignature":"60c5d743b71f79abe48c7183ada4b451",
#     "currency": "UAH",
#     "productName": ["Product name"],
#     "productCount": ["1"],
#     "clientFirstName": "John",
#     "clientLastName": "Doe",
#     "clientEmail": "johndoe@example.com",
#     "clientPhone": "1234567890",
#     "serviceUrl": "YOUR_SERVICE_URL",
#     "returnUrl": "YOUR_RETURN_URL",
#     "language": "en",
#     "orderDate": 1421412898,
#     "productPrice":["120"],
#     "orderTimeout": "3600",
#     "cardCvv": "123"
# }

allObjects = ['Одноразовая электронная сигарета Airis Lux P5000 Pina Colada', 'Одноразовая электронная сигарета R&M Legend 10000 затяжек Big Bang Fruit', 'Одноразовая сигарета Joyetech VAAL MAX Lush Ice', 'Одноразовая сигарета Joyetech VAAL GLAZ6500 Passion Fruit Orange Guava', 'Одноразовая сигарета Joyetech VAAL EP4500 Cotton Candy', 'Одноразовая сигарета Joyetech VAAL EP4500 Peach Mango Watermelon', 'Одноразовая электронная сигарета Elf Bar BC3500 3500 затяжек Cranberry Grape', 'Chaser Salt for Pods 15 мл 50 мг (5.0%) Bali Triple Shot', 'Chaser Salt - Blackcurrant Menthol (Черная смородина с ментолом) 10мл 30 мг (3.0%)', '3Ger Salt 15 мл 35 мг (3,5%) Apple Caramel']
random_elements = random.sample(allObjects, 5)
fu_str="test_merch_n1;www.market.ua;DH1679956995;1415379863;158;UAH;Процессор Intel Core i5-4670 3.4GHz;Память Kingston DDR3-1600 4096MB PC3-12800;1;1;1000;547.36"
new_str=fu_str.encode()
data = {
"transactionType":"CREATE_INVOICE",
"merchantAccount":"test_merch_n1",
"merchantAuthType":"SimpleSignature",
"merchantDomainName":"www.market.ua",
# "merchantSignature":"60c5d743b71f79abe48c7183ada4b451",
"apiVersion":1,
"language":"ru",
"serviceUrl":"https://eovbu9r2zfhhsp8.m.pipedream.net",
"orderReference":"DH16799571110",
"orderDate":1415379863,
"amount":500,
"currency":"UAH",
"orderTimeout": 60,
"productName": random_elements,
"productPrice":[1000,547, 432, 234, 324],
"productCount":[1,1, 1,1,1],
"paymentSystems": "card;privat24",
"clientFirstName":"Bulba",
"clientLastName":"Taras",
"clientEmail":"rob@mail.com",
"clientPhone":"380556667788"
}

# response=requests.get(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string=test_merch_n1%3Bwww.market.ua%3BDH1679956997%3B1415379863%3B158%3BUAH%3B%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D1%80%20Intel%20Core%20i5-4670%203.4GHz%3B%D0%9F%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20Kingston%20DDR3-1600%204096MB%  productPrice   20PC3-12800%3B1%3B1%3B1000%3B547&key=flk3409refn54t54t*FNJRET')
def create_signature(data:dict):
    response=requests.get(f'https://wiki.wayforpay.com/wiki/default/generate-hmac?string={data["merchantAccount"]}%3B{data["merchantDomainName"]}%3B{data["orderReference"]}%3B{data["orderDate"]}%3B{data["amount"]}%3B{data["currency"]}%3B{"%3B".join(data["productName"])}%3B{"%3B".join(str(i) for i in data["productCount"])}%3B{"%3B".join(str(i) for i in data["productPrice"])}&key=flk3409refn54t54t*FNJRET')
    return response.text
signature=create_signature(data)
data["merchantSignature"]=signature


response = requests.post(url, json.dumps(data))
json_obj = json.loads(response.text)
url = json_obj["invoiceUrl"].replace("\\","")
print(url)

# data_for_check={ 
# "merchantAccount":"test_merch_n1",
# "orderReference":"myOrder1",
# "merchantSignature":"DH1679957002",
# "amount":"1547.36",
# "currency":"UAH",
# "authCode":"541963",
# "email":"client@mail.ua",
# "phone":"380501234567",
# "createdDate":"",
# "processingDate":"",
# "cardPan":"4102****8217",
# "cardType":"visa",
# "issuerBankCountry":"980",
# "issuerBankName":"Privatbank",
# "recToken":"",
# "transactionStatus":"Approved",
# "reason":"1100",
# "reasonCode":"",
# "fee":"",
# "paymentSystem":"card"
# }

