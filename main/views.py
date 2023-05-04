from django.shortcuts import render
import requests
from main.models import Podik, NovaPost, Filters, Areas_and_costs, Offers, Users, PaymentMethod
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from .filters import PodFilter
from .forms import UpdatePriceForm, UpdateVisibilityForm, UpdateMessageForm
from django.urls import reverse
from django.http import HttpResponse
from django_filters.views import FilterView
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
#localStorage = localStoragePy('general2286.pythonanywhere.com', 'db.sqlite3')
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

bot = Bot(token="6075679825:AAGrgD6b9hybk9EoNue44k1ZPW8paFJCs5M")
dp = Dispatcher(bot)

def add_notification_to_user(request):
    pod_id = request.GET.get('id')
    tg_id = request.GET.get('user_id')

    pod = Podik.objects.get(id=pod_id)
    subscribers = pod.subscribers
    new_subscribers = ""
    if subscribers != None:
        if tg_id in subscribers.split(';'):
            return JsonResponse(data={})
    
        new_subscribers = subscribers + tg_id + ';'

    new_subscribers = tg_id + ';'
    Podik.objects.filter(id=pod_id).update(subscribers=new_subscribers)
    return JsonResponse(data={})

async def send_photo(chat_id,photo, text):
    # await bot.send_message(chat_id=chat_id, text=text)
    with open("image.png", 'rb') as f:
        await bot.send_photo(chat_id=chat_id,photo=f, caption=text)
    print(chat_id)

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)
def update_message(request):
    if request.method == 'POST':
        print(request.POST)
        form = UpdateMessageForm(request.POST, request.FILES)
        if form.is_valid():
            data = {}
            for key in request.POST.keys():
                if key.startswith('id'):
                    data[key[2:]] = request.POST[key]
                    print("sosat"+str(data[key[2:]]))
                    print("sosat"+str(key))
            print(data.values())
            temp = []
            for i in data.values():
                print(i)
                temp.append(i)
            new_visibility = request.POST.get('message')
            messages.success(request, f'Successfully updated {len(temp)} products')
            print(f"new_visibility = {new_visibility}")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # Generate a unique file name
            try:
                image_file = request.FILES['image']
                # Open a new file object and write the image data to the file
                with open("image.png", 'wb+') as destination:
                    for chunk in image_file.chunks():
                        destination.write(chunk)
                for q in temp:
                    future = asyncio.ensure_future(send_photo(chat_id=Users.objects.all().filter(tg_id =q)[0].tg_id, text=new_visibility, photo="image.png"))
                    Users.objects.all().filter(tg_id = q).update(message_text = "")
                loop.run_until_complete(future)
                loop.close()
                res = Users.objects.filter(name__in=temp)
                res.update(message_text = new_visibility)
                return redirect(reverse('admin:index'))
            except:
                for q in temp:
                    future = asyncio.ensure_future(send_message(chat_id=Users.objects.all().filter(tg_id =q)[0].tg_id, text=new_visibility))
                    Users.objects.all().filter(tg_id = q).update(message_text = "")
                loop.run_until_complete(future)
                loop.close()
                res = Users.objects.filter(name__in=temp)
                res.update(message_text = new_visibility)
                return redirect(reverse('admin:index'))

    return render(request, 'update_message.html', {'form': form})

def get_image(request):
    url = request.GET.get('url')
    response = requests.get(url)
    headers = {'Content-Type': 'image/jpeg', 'Access-Control-Allow-Origin': '*'}
    return HttpResponse(response.content, status=200, headers=headers)

def my_views(request):

    if  request.method == 'POST':
        data = request.POST.get('price')
        print(f"data = {data}")
        # items = localStorage.getItem("ids")
        # for pod in Podik.objects.all():
        #     if pod.id in items:
        #         pod.price = data
        response_data = {'result': 'success'}
        #localStorage.clear()
        print(response_data)
        return JsonResponse(response_data)
    else:
        response_data = {'error': 'Invalid request'}
        #localStorage.clear()
        return JsonResponse(response_data)
    

def update_price(request):
    if request.method == 'POST':
        form = UpdatePriceForm(request.POST)
        if form.is_valid():

            data = {}
            for key in request.POST.keys():
                if key.startswith('id'):
                    data[key[2:]] = request.POST[key]
            print(data.values())
            temp = []
            for i in data.values():
                print(i)
                temp.append(i)
            new_price = request.POST.get('price')
            new_quantity = request.POST.get('quantity_in_stock')
            new_available = request.POST.get('available')
            messages.success(request, f'Successfully updated {len(temp)} products')
            print(f"new_price = {new_price}")
            res = Podik.objects.filter(id__in=temp)
            if(new_price != ""):
                res.update(price=new_price)
            if(new_quantity != ""):
                res.update(quantity_in_stock=new_quantity)
            res.update(available = new_available)
            return redirect(reverse('admin:index'))
    else:
        print("321")
        selected_ids = request.GET.getlist('selected_ids')
        products = Podik.objects.filter(id__in=selected_ids)
        initial_price = products.first().price if products.exists() else 0
        form = UpdatePriceForm(initial={'price': initial_price})

    return render(request, 'update_price.html', {'form': form})

def update_visibility(request):
    if request.method == 'POST':
        form = UpdateVisibilityForm(request.POST)
        if form.is_valid():
            data = {}
            for key in request.POST.keys():
                if key.startswith('id'):
                    data[key[2:]] = request.POST[key]
                    print("sosat"+str(data[key[2:]]))
                    print("sosat"+str(key))
            print(data.values())
            temp = []
            for i in data.values():
                print(i)
                temp.append(i)
            new_visibility = request.POST.get('visible')
            messages.success(request, f'Successfully updated {len(temp)} products')
            print(f"new_visibility = {new_visibility}")
            res = Filters.objects.filter(name__in=temp)
            res.update(visible = new_visibility)
            return redirect(reverse('admin:index'))

    return render(request, 'update_visibility.html', {'form': form})

def novaPost(request):
    novaPost = serializers.serialize('json', NovaPost.objects.all())
    context = {"novaPost":novaPost,}
    return JsonResponse(context)
   
def novaPosttest(request):
    novaPost = serializers.serialize('json', NovaPost.objects.all())
    context = {"novapost":novaPost,}
    return render(request, "main/homepage.html", context)

def filter_data(request):
    filtered_data = Podik.objects.all()
    filter = PodFilter(request.GET, queryset=filtered_data)
    data = list(sorted(filter.qs.values(), key= lambda x: not x['available']))
    return JsonResponse({'data': data})

#при изменении в бд запускать этот код еще раз
#или попросить код егора
# class MyFilterView(FilterView):
#   model = Podik
#   filterset_class = PodFilter
#   print("23232")
#   template_name = "homepage.html"

#   def get(self, request, *args, **kwargs):
#     self.object_list = self.get_queryset()
#     self.object_list = self.filterset_class(request.GET, queryset=self.object_list).qs
#     context = self.get_context_data(object_list=self.object_list)
#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#       # Если запрос является AJAX-запросом, вернуть только часть шаблона
#       return render(request, "main/homepage.html", context)
#     else:
#       # В противном случае, вернуть полный шаблон
#       return self.render_to_response(context)

def heater(request):
    return render(request, 'main/heater.html', {})

def iqos(request):
    context = {
        "pods": Podik.objects.all().filter(categoryId = 208)
    }
    return render(request, 'main/iqos.html', context)

def glo(request):
    context = {
        "pods": Podik.objects.all().filter(categoryId = 282)
    }

def jouz(request):
    context = {
        "pods": Podik.objects.all().filter(categoryId = 282)
    }

def powerbanks(request):
    context = {
        "pods": Podik.objects.all().filter(categoryId = 282)
    }

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]['available']
    left = []
    right = []
    equal = []
    
    for item in arr:
        if not item['available']:
            right.append(item)
        elif item['available'] and item['available'] != pivot:
            left.append(item)
        else:
            equal.append(item)
    
    return quicksort(right) + equal + quicksort(left)

def load_more(request):
    podfilter = PodFilter(request.GET, queryset=Podik.objects.all())
    name = request.GET.get('name')
    total_item_str = request.GET.get('total_item')
    print(total_item_str)
    total_item = int(total_item_str)
    print(name, total_item)
    sorted_all = Podik.objects.all().order_by("-available")
    offers = {
        # 'pod':list((podfilter.qs.values())[total_item:total_item+50]),
        # 'pods':list((allObjects.filter(categoryId=220).values())[total_item:total_item+50]),
        # 'devices':list((allObjects.filter(categoryId=221).values())[total_item:total_item+50]),
        # 'cartridges':list((allObjects.filter(categoryId=222).values())[total_item:total_item+50]),
        # 'disposable':list((allObjects.filter(categoryId=239).values())[total_item:total_item+50]),
        # 'elf_bar':list((allObjects.filter(categoryId=287).values())[total_item:total_item+50]),
        # 'hqd':list((allObjects.filter(categoryId=288).values())[total_item:total_item+50]),
        # 'liquids':list((allObjects.filter(categoryId=208).values())[total_item:total_item+50]),
        # 'ukrainian_salt':list((allObjects.filter(categoryId=236).values())[total_item:total_item+50]),
        # 'premium_salt':list((allObjects.filter(categoryId=237).values())[total_item:total_item+50]),

        # 'pod':list(podfilter.qs.values().order_by("-available")[total_item:total_item+50]),
        # 'pods': list(allObjects.filter(categoryId=220).values().order_by("-available")[total_item:total_item+50]),
        # 'devices':list(allObjects.filter(categoryId=221).values().order_by("-available")[total_item:total_item+50]),
        # 'cartridges':list(allObjects.filter(categoryId=222).values().order_by("-available")[total_item:total_item+50]),
        # 'disposable':list(allObjects.filter(categoryId=239).values().order_by("-available")[total_item:total_item+50]),
        # 'elf_bar':list(allObjects.filter(categoryId=287).values().order_by("-available")[total_item:total_item+50]),
        # 'hqd':list(allObjects.filter(categoryId=288).values().order_by("-available")[total_item:total_item+50]),
        # 'liquids':list(allObjects.filter(categoryId=208).values().order_by("-available")[total_item:total_item+50]),
        # 'ukrainian_salt':list(allObjects.filter(categoryId=236).values().order_by("-available")[total_item:total_item+50]),
        # 'premium_salt':list(allObjects.filter(categoryId=237).values().order_by("-available")[total_item:total_item+50]),

        'pod':list(podfilter.qs.order_by("-available").values()[total_item:total_item+50]),
        'pods':list(sorted_all.filter(categoryId=220).values()[total_item:total_item+50]),
        'devices':list(sorted_all.filter(categoryId=221).values()[total_item:total_item+50]),
        'cartridges':list(sorted_all.filter(categoryId=222).values()[total_item:total_item+50]),
        'disposable':list(sorted_all.filter(categoryId=239).values()[total_item:total_item+50]),
        'elf_bar':list(sorted_all.filter(categoryId=287).values()[total_item:total_item+50]),
        'hqd':list(sorted_all.filter(categoryId=288).values()[total_item:total_item+50]),
        'liquids':list(sorted_all.filter(categoryId=208).values()[total_item:total_item+50]),
        'ukrainian_salt':list(sorted_all.filter(categoryId=236).values()[total_item:total_item+50]),
        'premium_salt':list(sorted_all.filter(categoryId=237).values()[total_item:total_item+50]),
    }

    data = {
        "offer": offers[name],
    }
    return JsonResponse(data=data)


def homepage(request, tg_id):
    try:
        fill = serializers.serialize('json', Offers.objects.all().filter(tg_id = tg_id)[0])
    except:
        fill = serializers.serialize('json', Offers.objects.all().filter(tg_id = tg_id))
    podfilter = PodFilter(request.GET, queryset=Podik.objects.all())
    print('aaaaaaaaaaaa')
    users = serializers.serialize('json', Users.objects.all().filter(tg_id=tg_id))
    areas_and_costs = serializers.serialize('json', Areas_and_costs.objects.all())
    filter_visibility = serializers.serialize('json', Filters.objects.all())
    novaPost = serializers.serialize('json', NovaPost.objects.all())
    allObjects = Podik.objects.all()
    # pods = serializers.serialize('json', podfilter.qs.order_by("-available")[:50])
    # pod_system = serializers.serialize('json', allObjects.filter(categoryId = 220).order_by("-available")[:50])
    # devices = serializers.serialize('json', allObjects.filter(categoryId = 221).order_by("-available")[:50])
    # disposable = serializers.serialize('json', allObjects.filter(categoryId = 239).order_by("-available")[:50])
    # cartridges = serializers.serialize('json', allObjects.filter(categoryId = 222).order_by("-available")[:50])
    # liquids = serializers.serialize('json', allObjects.filter(categoryId = 208).order_by("-available")[:50])
    # elf_bar = serializers.serialize('json', allObjects.filter(categoryId = 287).order_by("-available")[:50])
    # hqd = serializers.serialize('json', allObjects.filter(categoryId = 288).order_by("-available")[:50])
    # ukrainian_salt = serializers.serialize('json', allObjects.filter(categoryId = 236).order_by("-available")[:50])
    # premium_salt = serializers.serialize('json', allObjects.filter(categoryId = 237).order_by("-available")[:50])
    payment_methods = serializers.serialize('json', PaymentMethod.objects.all())
    # sorted_all = sorted(Podik.objects.all(), key= lambda x: not x.available)
    sorted_all = Podik.objects.all().order_by("-available")
    pods = serializers.serialize('json', sorted_all[:50])
    pod_system = serializers.serialize('json', sorted_all.filter(categoryId = 220)[:50])
    devices = serializers.serialize('json', sorted_all.filter(categoryId = 221)[:50])
    disposable = serializers.serialize('json', sorted_all.filter(categoryId = 239)[:50])
    cartridges = serializers.serialize('json', sorted_all.filter(categoryId = 222)[:50])
    liquids = serializers.serialize('json', sorted_all.filter(categoryId = 208)[:50])
    elf_bar = serializers.serialize('json', sorted_all.filter(categoryId = 287)[:50])
    hqd = serializers.serialize('json', sorted_all.filter(categoryId = 288)[:50])
    ukrainian_salt = serializers.serialize('json', sorted_all.filter(categoryId = 236)[:50])
    premium_salt = serializers.serialize('json', sorted_all.filter(categoryId = 237)[:50])
    
    context = {
        "users": users,
        "fill": fill,
        "filter_visibility": filter_visibility,
        "filter":podfilter.form,
        "pod": pods,
        "pod_system":pod_system,
        "devices":devices,
        "disposable":disposable,
        "cartridges":cartridges,
        "liquids":liquids,
        "elf_bar":elf_bar,
        "hqd":hqd,
        "ukrainian_salt":ukrainian_salt,
        "premium_salt":premium_salt,
        "novapost":novaPost,
        "areas_and_costs": areas_and_costs,
        "payment_methods": payment_methods,
    }
    return render(request, 'main/homepage.html', context)


def my_view(request):
    if request.method == 'GET':
        podfilter = PodFilter(request.GET, queryset=Podik.objects.all())
        pods = serializers.serialize('json', podfilter.qs[:50])
        context = {'filter': pods}
        return render(request, 'main/homepage.html', context)
    
from django.http import JsonResponse

def clear_filters(request):
    # Удаляем все параметры фильтров
    request.GET._mutable = True
    request.GET.clear()
    request.GET._mutable = False

    # Генерируем HTML для фильтров
    filters_html = render_to_string('homepage.html', {'filters': podfilter.form})
    podfilter = PodFilter(request.GET, queryset=Podik.objects.all())
    # Возвращаем данные в формате JSON
    return JsonResponse({'filters_html': filters_html})