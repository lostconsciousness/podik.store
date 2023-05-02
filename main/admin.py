from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from .models import *
from bs4 import BeautifulSoup
from utils import DBManager
from django.http import HttpResponse
import csv
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.template.response import TemplateResponse
from django.http import JsonResponse
from localStoragePy import localStoragePy
from .forms import UpdatePriceForm, UpdateVisibilityForm, UpdateMessageForm
from django.db.models import QuerySet
import asyncio
from .models import Users
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions

bot = Bot(token="6075679825:AAGrgD6b9hybk9EoNue44k1ZPW8paFJCs5M")
dp = Dispatcher(bot)
#localStorage = localStoragePy('general2286.pythonanywhere.com', 'db.sqlite3')

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

class CashbackAdmin(admin.ModelAdmin):
    list_display=('percentage',)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class UsersAdmin(admin.ModelAdmin):
    @admin.action(description='Download')
    def download_users_with_referral_count_gt_one(self, request, queryset):
        users = Users.objects.filter(referral_count__gt=1)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_with_referral_count_gt_one.csv"'
        writer = csv.writer(response)
        writer.writerow(['username', 'email', 'referral_count'])
        for user in users:
            writer.writerow([user.username, user.email, user.referral_count])
        return response
    @admin.action(description='Масово надіслати повідомлення')
    def send_message_to_telegram(self, request, queryset):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for q in queryset:
            future = asyncio.ensure_future(send_message(chat_id=q.tg_id, text=q.message_text))
            Users.objects.all().filter(tg_id = q.tg_id).update(message_text = "")
        loop.run_until_complete(future)
        loop.close()
        self.message_user(request, 'Messages were sent to Telegram.')
    @admin.action(description='Масово надіслати повідомлення')
    def update_message(self, request, queryset: QuerySet):
        form = UpdateMessageForm()
        j=0
        data_dict={}
        for i in queryset:
            data_dict[f"id{j}"]=i.tg_id
            j+=1
        # print(data_dict)
        return render(request, 'admin/update_message.html', {"my_data":data_dict, 'form': form})
    list_display = ('username','phone_number', 'name', 'referral_count', 'cashback_amount')
    list_display_links = ('username','phone_number', 'name', 'referral_count', 'cashback_amount')
    readonly_fields = ('username','phone_number', 'name', 'referral_count', 'cashback_amount')
    exclude = ('message_text',)
    actions = [update_message, download_users_with_referral_count_gt_one]

class XmlImportForm(forms.Form):
    xml_upload = forms.FileField()

#start
class PriceForm(forms.Form):
    price = forms.CharField(max_length=255)

class Areas_and_costsAdmin(admin.ModelAdmin):
    list_display = ('area', 'cost_for_warehouse', 'cost_for_post', 'cost_for_adress')
    fields = ('area', 'cost_for_warehouse', 'cost_for_post', 'cost_for_adress')
    list_display_links = ('area', 'cost_for_warehouse', 'cost_for_post', 'cost_for_adress')
    readonly_fields = ('area',)

class FiltersAdmin(admin.ModelAdmin):
    actions = ['update_price']
    # def update_price(self, request, queryset):
    #     # Перенаправляет на страницу обновления цены.
    #     return HttpResponseRedirect(reverse('admin:update_price', args=[queryset.values_list('id', flat=True)]))
    # update_price.short_description = 'Обновить цену'
    def update_price(self, request, queryset: QuerySet):
        # Перенаправляет на страницу обновления цены.
        # return HttpResponseRedirect(reverse('update_price', args=[queryset.values_list('id', flat=True)])) 
        form = UpdateVisibilityForm()
        # print(list(queryset))
        j=0
        data_dict={}
        for i in queryset:
            data_dict[f"id{j}"]=i.name
            j+=1
        # print(data_dict)
        return render(request, 'admin/update_visibility.html', {"my_data":data_dict, 'form': form})
    update_price.short_description = "Оновити параметри"
    list_display = ('name', 'visible')
    fields = ('name', 'visible')
    list_display_links = ('name', 'visible')
    readonly_fields = ('name',)

class OffersAdmin(admin.ModelAdmin):
    list_display = ('id','username','phone_number', 'call','name','offer', 'amount', 'area', 'city', 'warehouse','payment_method', 'delivery_method', 'comment')
    list_display_links = ('id','username','phone_number', 'call', 'name','offer', 'amount', 'area', 'city', 'warehouse','payment_method', 'delivery_method', 'comment')
    readonly_fields = ('id','username','phone_number', 'call', 'name','offer', 'amount', 'area', 'city', 'warehouse', 'products', 'comment', 'payment_method', 'delivery_method')
    search_fields = ('id', 'phone_number',)





class PodikAdmin(admin.ModelAdmin):
    actions = ['update_price']
    # def update_price(self, request, queryset):
    #     # Перенаправляет на страницу обновления цены.
    #     return HttpResponseRedirect(reverse('admin:update_price', args=[queryset.values_list('id', flat=True)]))
    # update_price.short_description = 'Обновить цену'
    def update_price(self, request, queryset: QuerySet):
        # Перенаправляет на страницу обновления цены.
        # return HttpResponseRedirect(reverse('update_price', args=[queryset.values_list('id', flat=True)])) 
        form = UpdatePriceForm()
        # print(list(queryset))
        j=0
        data_dict={}
        for i in queryset:
            data_dict[f"id{j}"]=i.id
            j+=1
        # print(data_dict)
        return render(request, 'admin/update_price.html', {"my_data":data_dict, 'form': form})
    update_price.short_description = "Оновити параметри"
    #end


    list_display = ('id','name','price', 'currencyId', 'available', 'quantity_in_stock','param',  'get_html_photo')
    list_display_links = ('id','name','price', 'available', 'quantity_in_stock','currencyId')
    search_fields = ('id','name', 'price', 'param', 'picture')
    list_filter = ('available',)
    fields = ('name', 'id', 'available', 'price', 'currencyId', 'categoryId', 'vendorCode', 'quantity_in_stock', 'url', 'picture', 'get_html_photo', 'flavour' , 'nicotine_strength', 'fluid_volume', 'battery_capacity', 'cartridge_capacity', 'resistance', 'power', 'atomizer_volume', 'max_power', 'puffs_number', 'rechargeable', 'compatibility_selection')
    readonly_fields = ('get_html_photo', )
    def get_html_photo(self, object):
        return mark_safe(f"<img src = {object.picture} width = 50>")
    
    get_html_photo.short_description = 'Фото'
 
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-xml/', self.upload_xml), path('update-price/', self.update_price)]
        return new_urls + urls
    
    def upload_xml(self, request):
        if request.method == "POST":
            xml_file = request.FILES["xml_upload"]
            # with open(xml_file,'r') as f:
            #     data = f.read()
            # tree = ET.parse(xml_file)
            # root = tree.getroot()
            file_data = xml_file.read().decode()
            with open('offer.xml', 'w', encoding='utf-8') as f:
                f.write(file_data)


            dbm = DBManager()
            dbm.addXmlToDB()


            # with open('offer.xml', 'r', encoding='utf-8') as f:
            #     data = f.read()
            # bs_data = BeautifulSoup(data, "xml")
            # print(type(bs_data.find('offer').find('vendorCode').text))
            # print(type(bs_data.find('offer')['available']))
            # offers = file.getElementsByTagName('name')
        form = XmlImportForm()
        data = {"form": form}
        return render(request, "admin/xml_upload.html", data)
# 

class PaymentAdmin(admin.ModelAdmin):
    list_display=('name','fee')


admin.site.register(PaymentMethod, PaymentAdmin)
admin.site.register(Podik, PodikAdmin)
admin.site.register(Offers, OffersAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Areas_and_costs, Areas_and_costsAdmin)
admin.site.register(Filters, FiltersAdmin)
admin.site.register(CashbackPercentage, CashbackAdmin)
admin.site.site_title = 'сторінка адміністрації'
admin.site.site_header = 'Cторінка адміністрації'