from .models import Podik
from django import forms
from django.forms import TextInput, Select
from django.db.models import Q
import django_filters
from django_filters.widgets import RangeWidget
from .models import Filters
from utils import all_categories

def all_flavours():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    for pod in allObjects:
        res = []
        #print(pod.flavour)
        if pod.flavour not in povtor and pod.flavour != "-":
            povtor.append(pod.flavour)
            res.append(pod.flavour)
            res.append(pod.flavour)
            result.append(tuple(res))
    print(result)
    return result

def all_disposable_flavours():
    allObjects = Podik.objects.all().filter(categoryId = 239)
    all_hqds = Podik.objects.all().filter(categoryId = 288)
    all_ukrainian = Podik.objects.all().filter(categoryId = 236)
    all_liquids = Podik.objects.all().filter(categoryId = 208)
    all_elfs = Podik.objects.all().filter(categoryId = 287)
    result = []
    povtor = []

    hqd_povtor = []
    hqd_result = []

    ukrainian_povtor = []
    ukrainian_result = []

    liquids_povtor = []
    liquids_result = []

    elfs_povtor = []
    elfs_result = []

    for pod in all_ukrainian:
        ukrainian_res = []
        if pod.flavour not in ukrainian_povtor and pod.flavour != "-":
                ukrainian_povtor.append(pod.flavour)
                ukrainian_res.append(pod.flavour)
                ukrainian_res.append(pod.flavour)
                ukrainian_result.append(tuple(ukrainian_res))
    for pod in all_liquids:
        liquids_res = []
        if pod.flavour not in liquids_povtor and pod.flavour != "-":
                liquids_povtor.append(pod.flavour)
                liquids_res.append(pod.flavour)
                liquids_res.append(pod.flavour)
                liquids_result.append(tuple(liquids_res))
    for pod in all_elfs:
        elfs_res = []
        if pod.flavour not in elfs_povtor and pod.flavour != "-":
                elfs_povtor.append(pod.flavour)
                elfs_res.append(pod.flavour)
                elfs_res.append(pod.flavour)
                elfs_result.append(tuple(elfs_res))
    for pod in all_hqds:
        hqd_res = []
        if pod.flavour not in hqd_povtor and pod.flavour != "-":
                hqd_povtor.append(pod.flavour)
                hqd_res.append(pod.flavour)
                hqd_res.append(pod.flavour)
                hqd_result.append(tuple(hqd_res))
    for pod in allObjects:
        res = []
        hqd_res = []
        #print(pod.flavour)
        if pod.flavour not in povtor and pod.flavour != "-":
            povtor.append(pod.flavour)
            res.append(pod.flavour)
            res.append(pod.flavour)
            result.append(tuple(res))
    print(result)
    all_results = []
    all_results.append(hqd_result)
    all_results.append(result)
    all_results.append(elfs_result)
    all_results.append(liquids_result)
    all_results.append(ukrainian_result)
    return all_results

def all_strength():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.nicotine_strength[:2] not in pp and pod.nicotine_strength[:2] != "-"and pod.nicotine_strength[:2] != "" and pod.nicotine_strength[:2] != "00":
            povtor.append(pod.nicotine_strength)
            pp.append(pod.nicotine_strength[:2])

    sort = sorted(pp)
    povtor = sorted(povtor)
    for pod in sort:
        res = []
        res.append(pod)
        res.append(pod + ' мг')
        result.append(tuple(res))
    return result

def all_fluid_volume():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.fluid_volume.split(' ')[0].replace("мл","") not in pp and pod.fluid_volume != "-"and pod.fluid_volume != "":
            pp.append(pod.fluid_volume.split(' ')[0].replace("мл",""))
            povtor.append(float(pod.fluid_volume.split(' ')[0].replace("мл","")))
    sort = sorted(povtor)
    for pod in sort:
        res = []
        strpod = str(pod)
        if strpod.split('.')[1]=='0':
            strpod = strpod.split('.')[0]
        res.append(strpod)
        res.append(strpod + ' мл.')
        result.append(tuple(res))
    return result

def all_battery_capacity():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.battery_capacity not in pp and pod.battery_capacity != "-"and pod.battery_capacity != "":
            pp.append(pod.battery_capacity)
            povtor.append(int(pod.battery_capacity.split(' ')[0]))
    sort = sorted(povtor)
    # print(sort)
    for pod in sort:
        res = []
        strpod = str(pod)
        res.append(strpod)
        res.append(strpod + ' mAh')
        result.append(tuple(res))
    #print(result)
    return result

def all_resistance():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.resistance.split(' ')[0] not in pp and pod.resistance != "-"and pod.resistance != "":
            pp.append(pod.resistance.split(' ')[0])
            povtor.append(float(pod.resistance.split(' ')[0]))
    sort = sorted(povtor)
    for pod in sort:
        res = []
        strpod = str(pod)
        res.append(strpod)
        res.append(strpod + ' Ом')
        result.append(tuple(res))
    return result

def all_power():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    for pod in allObjects:
        res = []
        #print(pod.flavour)
        if pod.power not in povtor and pod.power != "-"and pod.power != "":
            povtor.append(pod.power)
            res.append(pod.power)
            res.append(pod.power)
            result.append(tuple(res))
    #print(result)
    return result

def all_atomizer_volume():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.fluid_volume.split(' ')[0].replace("мл","") not in pp and pod.fluid_volume != "-"and pod.fluid_volume != "":
            pp.append(pod.fluid_volume.split(' ')[0].replace("мл",""))
            povtor.append(float(pod.fluid_volume.split(' ')[0].replace("мл","")))
    sort = sorted(povtor)
    for pod in sort:
        res = []
        strpod = str(pod)
        if strpod.split('.')[1]=='0':
            strpod = strpod.split('.')[0]
        res.append(strpod)
        res.append(strpod + ' мл.')
        result.append(tuple(res))
    return result

def all_max_power():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.max_power.split(' ')[0] not in pp and pod.max_power != "-"and pod.max_power != "":
            pp.append(pod.max_power.split(' ')[0])
            povtor.append(int(pod.max_power.split(' ')[0]))
    sort = sorted(povtor)
    for pod in sort:
        res = []
        strpod = str(pod)
        res.append(strpod)
        res.append(strpod + ' Вт')
        result.append(tuple(res))
    return result

def all_puffs_number():
    allObjects = Podik.objects.all()
    result = []
    povtor = []
    pp = []
    sort = []
    for pod in allObjects:
        if pod.puffs_number not in pp and pod.puffs_number != "-"and pod.puffs_number != "":
            pp.append(pod.puffs_number)
            try:
                povtor.append(int(pod.puffs_number))
            except:
                pass
    sort = sorted(povtor)
    for pod in sort:
        res = []
        strpod = str(pod)
        res.append(strpod)
        res.append(strpod)
        result.append(tuple(res))
    return result


class PodFilter(django_filters.FilterSet):
    categoryId = django_filters.ChoiceFilter(lookup_expr = "exact", choices = all_categories(), widget = Select(attrs = {'class': 'catId_input'}))
    price = django_filters.RangeFilter(widget = RangeWidget(attrs = {'class': 'price_input invisible'}))
    param = django_filters.ChoiceFilter(lookup_expr = "icontains",choices = tuple(all_flavours()), widget=Select(attrs = {'class': 'param_input visible'}))
    nicotine_strength = django_filters.MultipleChoiceFilter(lookup_expr = "contains",choices = tuple(all_strength()), widget= forms.CheckboxSelectMultiple(attrs = {'class': 'nicotine_strength invisible'}))
    fluid_volume = django_filters.MultipleChoiceFilter(lookup_expr = "icontains", choices = tuple(all_fluid_volume()), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'fluid_volume invisible'}))
    battery_capacity = django_filters.MultipleChoiceFilter(lookup_expr = "icontains", choices = tuple(all_battery_capacity()), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'battery_capacity invisible'}))
    resistance = django_filters.MultipleChoiceFilter(lookup_expr = 'icontains', choices = tuple(all_resistance()), widget = forms.CheckboxSelectMultiple(attrs = {'class':'resistance invisible'}))
    power = django_filters.MultipleChoiceFilter(lookup_expr = 'icontains', choices = tuple(all_power()), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'power invisible'}))
    atomizer_volume = django_filters.MultipleChoiceFilter(lookup_expr = 'icontains', choices = tuple(all_atomizer_volume()), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'atomizer_volume invisible'}))
    max_power = django_filters.MultipleChoiceFilter(lookup_expr = 'icontains', choices = tuple(all_max_power()), widget = forms.CheckboxSelectMultiple(attrs={'class': 'max_power invisible'}))
    puffs_number = django_filters.MultipleChoiceFilter(lookup_expr = 'icontains', choices = tuple(all_puffs_number()), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'puffs_number invisible'}))
    rechargeable = django_filters.MultipleChoiceFilter(lookup_expr = 'exact', choices = ((1,'Так'), (0,'Ні')), widget = forms.RadioSelect(attrs = {'class' : 'rechargeable invisible'}))
    hqd_flavour = django_filters.ChoiceFilter(lookup_expr = "icontains",choices = tuple(all_disposable_flavours()[0]), widget=Select(attrs = {'class': ' invisible', 'id': "hqd_flavour"}))
    disposable_flavour = django_filters.ChoiceFilter(lookup_expr = "icontains",choices = tuple(all_disposable_flavours()[1]), widget=Select(attrs = {'class': ' invisible', 'id': "disposable_flavour"}))
    elf_bar_flavour = django_filters.ChoiceFilter(lookup_expr = "icontains",choices = tuple(all_disposable_flavours()[2]), widget=Select(attrs = {'class': ' invisible', 'id': "elfs_flavour"}))
    liquids_flavour = django_filters.ChoiceFilter(lookup_expr = "icontains",choices = tuple(all_disposable_flavours()[3]), widget=Select(attrs = {'class': ' invisible', 'id': "liquids_flavour"}))
    ukrainian_flavour = django_filters.ChoiceFilter(lookup_expr = "icontains",choices = tuple(all_disposable_flavours()[4]), widget=Select(attrs = {'class': ' invisible', 'id': "ukrainian_flavour"}))


    class Meta:
        model = Podik
        fields = ({'price', 'categoryId', 'param', 'nicotine_strength', 'fluid_volume', 'resistance', 'power', 'atomizer_volume',
                    'max_power', 'puffs_number', 'rechargeable', 'hqd_flavour', 'disposable_flavour',
                    'elf_bar_flavour', 'liquids_flavour', 'ukrainian_flavour'})
    def filter_pod_system(self, queryset, name, price1):
        # print(price1)
        start = int(price1.start)
        stop = int(price1.stop)
        step = price1.step
        return queryset.filter(Q(price__gte = start)&Q(price__lte = stop))