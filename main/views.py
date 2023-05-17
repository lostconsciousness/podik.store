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
from django.db.models import F, IntegerField
from django.db.models.functions import Cast

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
        await bot.send_photo(chat_id=chat_id,photo=f, caption=text, parse_mode="HTML")

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
def update_message(request):
    if request.method == 'POST':
        form = UpdateMessageForm(request.POST, request.FILES)
        if form.is_valid():
            data = {}
            for key in request.POST.keys():
                if key.startswith('id'):
                    data[key[2:]] = request.POST[key]
            temp = []
            for i in data.values():
                temp.append(i)
            new_visibility = request.POST.get('message')
            messages.success(request, f'Successfully updated {len(temp)} products')
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
        # items = localStorage.getItem("ids")
        # for pod in Podik.objects.all():
        #     if pod.id in items:
        #         pod.price = data
        response_data = {'result': 'success'}
        #localStorage.clear()
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
            temp = []
            for i in data.values():
                temp.append(i)
            new_price = request.POST.get('price')
            new_quantity = request.POST.get('quantity_in_stock')
            new_available = request.POST.get('available')
            messages.success(request, f'Successfully updated {len(temp)} products')
            res = Podik.objects.filter(id__in=temp)
            if(new_price != ""):
                res.update(price=new_price)
            if(new_quantity != ""):
                res.update(quantity_in_stock=new_quantity)
            res.update(available = new_available)
            return redirect(reverse('admin:index'))
    else:
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
            temp = []
            for i in data.values():
                temp.append(i)
            new_visibility = request.POST.get('visible')
            messages.success(request, f'Successfully updated {len(temp)} products')
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
    total_item = int(total_item_str)
    sorted_all = Podik.objects.all().annotate(int_available = Cast("available", IntegerField())).order_by(F('int_available').desc(), F('id').asc() )
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

        'pod':list(podfilter.qs.annotate(int_available = Cast("available", IntegerField())).order_by(F('int_available').desc(), F('id').asc()).values()[total_item:total_item+50]),
        'pods':list(sorted_all.filter(categoryId=220).values()[total_item:total_item+50]),
        'devices':list(sorted_all.filter(categoryId=221).values()[total_item:total_item+50]),
        'cartridges':list(sorted_all.filter(categoryId=222).values()[total_item:total_item+50]),
        'disposable':list(sorted_all.filter(categoryId=239).values()[total_item:total_item+50]),
        'elf_bar':list(sorted_all.filter(categoryId=287).values()[total_item:total_item+50]),
        'hqd':list(sorted_all.filter(categoryId=288).values()[total_item:total_item+50]),
        'liquids':list(sorted_all.filter(categoryId=208).values()[total_item:total_item+50]),
        'ukrainian_salt':list(sorted_all.filter(categoryId=236).values()[total_item:total_item+50]),
        'premium_salt':list(sorted_all.filter(categoryId=237).values()[total_item:total_item+50]),
        'all_liquids': list(sorted_all.filter(categoryId=187).values()[total_item:total_item + 50]),
        'liquid_ukraine': list(sorted_all.filter(categoryId=200).values()[total_item:total_item + 50]),
        'liquid_import': list(sorted_all.filter(categoryId=199).values()[total_item:total_item + 50]),
        'liquid_base': list(sorted_all.filter(categoryId=284).values()[total_item:total_item + 50]),
        'liquid_aromat': list(sorted_all.filter(categoryId=191).values()[total_item:total_item + 50]),
        'liquid_nabor': list(sorted_all.filter(categoryId=286).values()[total_item:total_item + 50]),
        'box_mode': list(sorted_all.filter(categoryId=176).values()[total_item:total_item + 50]),
        'meh_mode': list(sorted_all.filter(categoryId=206).values()[total_item:total_item + 50]),
        'start_nabor_esigs': list(sorted_all.filter(categoryId=283).values()[total_item:total_item + 50]),
        'complect': list(sorted_all.filter(categoryId=173).values()[total_item:total_item + 50]),
        'bak': list(sorted_all.filter(categoryId=182).values()[total_item:total_item + 50]),
        'avtomaizer': list(sorted_all.filter(categoryId=172).values()[total_item:total_item + 50]),
        'dripki': list(sorted_all.filter(categoryId=183).values()[total_item:total_item + 50]),
        'isparik': list(sorted_all.filter(categoryId=178).values()[total_item:total_item + 50]),
        'battery': list(sorted_all.filter(categoryId=217).values()[total_item:total_item + 50]),
        'spiral': list(sorted_all.filter(categoryId=179).values()[total_item:total_item + 50]),
        'charge': list(sorted_all.filter(categoryId=185).values()[total_item:total_item + 50]),
        'case': list(sorted_all.filter(categoryId=215).values()[total_item:total_item + 50]),
        'vata': list(sorted_all.filter(categoryId=180).values()[total_item:total_item + 50]),
        'glass': list(sorted_all.filter(categoryId=181).values()[total_item:total_item + 50]),
        'drip_tip': list(sorted_all.filter(categoryId=204).values()[total_item:total_item + 50]),
        'namotka': list(sorted_all.filter(categoryId=214).values()[total_item:total_item + 50]),
        'voopoo': list(sorted_all.filter(categoryId=289).values()[total_item:total_item + 50]),
        'juul': list(sorted_all.filter(categoryId=205).values()[total_item:total_item + 50]),
        'juul_nabor': list(sorted_all.filter(categoryId=218).values()[total_item:total_item + 50]),
        'juul_cartridge': list(sorted_all.filter(categoryId=207).values()[total_item:total_item + 50]),
        'juul_aksesuar': list(sorted_all.filter(categoryId=223).values()[total_item:total_item + 50]),
        'logic': list(sorted_all.filter(categoryId=232).values()[total_item:total_item + 50]),
        'fich': list(sorted_all.filter(categoryId=279).values()[total_item:total_item + 50]),
        'joint': list(sorted_all.filter(categoryId=235).values()[total_item:total_item + 50]),
        'relx': list(sorted_all.filter(categoryId=241).values()[total_item:total_item + 50]),
        'vype': list(sorted_all.filter(categoryId=240).values()[total_item:total_item + 50]),
    }

    data = {
        "offer": offers[name],
    }
    return JsonResponse(data=data)

#сделать по-нормальному, тоесть засовывать в ссылку айди категории и из нее брать
def homepage(request, tg_id):
    try:
        fill = serializers.serialize('json', Offers.objects.all().filter(tg_id = tg_id)[0])
    except:
        fill = serializers.serialize('json', Offers.objects.all().filter(tg_id = tg_id))
    podfilter = PodFilter(request.GET, queryset=Podik.objects.all())
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
    sorted_all = Podik.objects.all().annotate(int_available = Cast("available", IntegerField())).order_by(F('int_available').desc(), F('id').asc() )
    pods = serializers.serialize('json', sorted_all[:50])
    pod_system = serializers.serialize('json', sorted_all.filter(categoryId=220)[:50])
    devices = serializers.serialize('json', sorted_all.filter(categoryId=221)[:50])
    disposable = serializers.serialize('json', sorted_all.filter(categoryId=239)[:50])
    cartridges = serializers.serialize('json', sorted_all.filter(categoryId=222)[:50])
    liquids = serializers.serialize('json', sorted_all.filter(categoryId=208)[:50])
    elf_bar = serializers.serialize('json', sorted_all.filter(categoryId=287)[:50])
    hqd = serializers.serialize('json', sorted_all.filter(categoryId=288)[:50])
    ukrainian_salt = serializers.serialize('json', sorted_all.filter(categoryId=236)[:50])
    premium_salt = serializers.serialize('json', sorted_all.filter(categoryId=237)[:50])
    all_liquds = serializers.serialize('json', sorted_all.filter(categoryId=187)[:50])
    liquid_ukraine = serializers.serialize('json', sorted_all.filter(categoryId=200)[:50])
    liquid_import = serializers.serialize('json', sorted_all.filter(categoryId=199)[:50])
    liquid_base = serializers.serialize('json', sorted_all.filter(categoryId=284)[:50])
    liquid_aromat = serializers.serialize('json', sorted_all.filter(categoryId=191)[:50])
    liquid_nabor = serializers.serialize('json', sorted_all.filter(categoryId=286)[:50])
    box_mode = serializers.serialize('json', sorted_all.filter(categoryId=176)[:50])
    meh_mode = serializers.serialize('json', sorted_all.filter(categoryId=206)[:50])
    start_nabor_esigs = serializers.serialize('json', sorted_all.filter(categoryId=283)[:50])
    complect = serializers.serialize('json', sorted_all.filter(categoryId=173)[:50])
    bak = serializers.serialize('json', sorted_all.filter(categoryId=182)[:50])
    avtomaizer = serializers.serialize('json', sorted_all.filter(categoryId=172)[:50])
    dripki = serializers.serialize('json', sorted_all.filter(categoryId=183)[:50])
    isparik = serializers.serialize('json', sorted_all.filter(categoryId=178)[:50])
    battery = serializers.serialize('json', sorted_all.filter(categoryId=217)[:50])
    spiral = serializers.serialize('json', sorted_all.filter(categoryId=179)[:50])
    charge = serializers.serialize('json', sorted_all.filter(categoryId=185)[:50])
    case = serializers.serialize('json', sorted_all.filter(categoryId=215)[:50])
    vata = serializers.serialize('json', sorted_all.filter(categoryId=180)[:50])
    glass = serializers.serialize('json', sorted_all.filter(categoryId=181)[:50])
    drip_tip = serializers.serialize('json', sorted_all.filter(categoryId=204)[:50])
    namotka = serializers.serialize('json', sorted_all.filter(categoryId=214)[:50])

    voopoo = serializers.serialize('json', sorted_all.filter(categoryId=289)[:50])
    juul = serializers.serialize('json', sorted_all.filter(categoryId=205)[:50])
    juul_nabor = serializers.serialize('json', sorted_all.filter(categoryId=218)[:50])
    juul_cartridge = serializers.serialize('json', sorted_all.filter(categoryId=207)[:50])

    juul_aksesuar = serializers.serialize('json', sorted_all.filter(categoryId = 223)[:50])
    logic = serializers.serialize('json', sorted_all.filter(categoryId = 232)[:50])
    fich = serializers.serialize('json', sorted_all.filter(categoryId = 279)[:50])
    joint = serializers.serialize('json', sorted_all.filter(categoryId = 235)[:50])
    relx = serializers.serialize('json', sorted_all.filter(categoryId = 241)[:50])
    vype = serializers.serialize('json', sorted_all.filter(categoryId = 240)[:50])
    
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
        "all_liquds":all_liquds,
        "liquid_ukraine":liquid_ukraine,
        "liquid_import":liquid_import,
        "liquid_base":liquid_base,
        "avtomaizer":avtomaizer,
        "liquid_aromat":liquid_aromat,
        "liquid_nabor":liquid_nabor,
        "box_mode":box_mode,
        "complect":complect,
        "meh_mode":meh_mode,
        "start_nabor_esigs":start_nabor_esigs,
        "bak":bak,
        "dripki":dripki,
        "isparik":isparik,
        "battery":battery,
        "spiral":spiral,
        "charge":charge,
        "case":case,
        "vata":vata,
        "glass":glass,
        "drip_tip":drip_tip,
        "namotka":namotka,
        "voopoo":voopoo,
        "devices_pod":devices,
        "cartridge_pod":cartridges,
        "juul_nabor":juul_nabor,
        "juul_cartridge":juul_cartridge,
        "juul_aksesuar":juul_aksesuar,
        "logic":logic,
        "fich":fich,
        "joint":joint,
        "relx":relx,
        "vype":vype,
        "juul":juul,
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