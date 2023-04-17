from django.db.models import Avg
from .models import Shop, Inventory


def utilities(request):
    return concrete(request)


def concrete(request):

    CementPrice = float(Inventory.objects.aggregate(Avg('cement_price'))[
        'cement_price__avg'])
    SandPrice = float(Inventory.objects.aggregate(
        Avg('sand_price'))['sand_price__avg'])
    AggregatePrice = float(Inventory.objects.aggregate(Avg('aggregate_price'))[
        'aggregate_price__avg'])
    print('cementprice:', CementPrice, ' sandprice:',
          SandPrice, ' aggregateprice:', AggregatePrice)

    CementUnitsperTon = request.POST.get('CementUnitsperTon')
    if CementUnitsperTon is not None and CementUnitsperTon != '':
        CementUnitsperTon = float(CementUnitsperTon)
    else:
        # handle the case where the CementUnitsperTon value is missing or empty
        CementUnitsperTon = 0.0  # set a default value or raise an error

    SandUnitsperTon = request.POST.get('SandUnitsperTon')
    if SandUnitsperTon is not None and SandUnitsperTon != '':
        SandUnitsperTon = float(SandUnitsperTon)
    else:
        # handle the case where the SandUnitsperTon value is missing or empty
        SandUnitsperTon = 0.0  # set a default value or raise an error

    AggregateUnitsperTon = request.POST.get('AggregateUnitsperTon')
    if AggregateUnitsperTon is not None and AggregateUnitsperTon != '':
        AggregateUnitsperTon = float(AggregateUnitsperTon)
    else:
        # handle the case where the AggregateUnitsperTon value is missing or empty
        AggregateUnitsperTon = 0.0  # set a default value or raise an error

    num = request.POST.get('num')
    if num is not None and num != '':
        num = float(num)
        num = 0.01*num
    else:
        # handle the case where the num value is missing or empty
        num = 0.0  # set a default value or raise an error

    # CementPrice = float(request.POST.get('CementPrice'))
    # SandPrice = float(request.POST.get('SandPrice'))
    # AggregatePrice = float(request.POST.get('AggregatePrice'))
    # CementUnitsperTon = float(request.POST.get('CementUnitsperTon'))
    # SandUnitsperTon = float(request.POST.get('SandUnitsperTon'))
    # AggregateUnitsperTon = float(request.POST.get('AggregateUnitsperTon'))
    # num = float(request.POST.get('num'))
    ratios = {
        '15': [1, 3, 6],
        '20': [1, 2, 4],
        '25': [1, 1.5, 3],
        '30': [1, 1, 2]
    }

    concreteclass = request.POST.get('class')
    print(concreteclass)
    ratio = ratios.get(concreteclass)
    print(ratio)

    if ratio is None:
        ratio = [1, 1, 1]
        # raise ValueError('Invalid concrete class')
    TotalRatio = sum(ratio)
    print('sumratio:', TotalRatio)
    ComponentCement = 1.485 * CementUnitsperTon * CementPrice * ratio[0]
    ComponentSand = 1.605 * SandUnitsperTon * SandPrice * ratio[1]
    ComponentAggregate = 1.415 * \
        AggregateUnitsperTon * AggregatePrice * ratio[2]

    TotalCostof7cmofconcrete = ComponentCement + ComponentAggregate + ComponentSand
    print(TotalCostof7cmofconcrete)
    CostperCm = TotalCostof7cmofconcrete/TotalRatio
    print(CostperCm)
    addshrinkage = CostperCm + (0.45*CostperCm)
    print(addshrinkage)
    addlabour = addshrinkage + (0.3*addshrinkage)
    print(addlabour)
    addoverhead = addlabour + (num*addlabour)
    print(addoverhead)
    addVAT = addoverhead + (0.16*addoverhead)
    print(addVAT)
    ratepersm = 0.15*addVAT

    context = {'ratepersm': ratepersm}
    return context
