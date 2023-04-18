from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rates.models import Shop, Inventory
from rates.utils import utility
import json

class ShopInventoryView(APIView):
    authentication_classes = []
    permission_classes = []
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        inventory_data = Inventory.objects.all().aggregate(
            Avg('cement_price'), Avg('sand_price'), Avg('aggregate_price')
        )
        return Response({
            'cement_price_avg': inventory_data['cement_price__avg'],
            'sand_price_avg': inventory_data['sand_price__avg'],
            'aggregate_price_avg': inventory_data['aggregate_price__avg'],
        })

class ComponentsView(APIView):
    authentication_classes = []
    permission_classes = []
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        components = ['Concrete', 'Bricks', 'Steel']
        return Response(components)


class RatesView(APIView):
	authentication_classes = []
	permission_classes = []

	@csrf_exempt
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
	    data = json.loads(request.body)
	    component = data['component']
	    selected_class = data['class']
	    labour_costs = data['labourCosts']
	    profit_overheads = data['profitOverheads']
	    print('component:', component, 'selected_class:', selected_class, 'labour_costs:', labour_costs, 'profit_overheads: ',profit_overheads)
	    
	    # Process the data and calculate the rate
	    rate = utility(component=component, selected_class=selected_class, labour_costs=labour_costs, profit_overheads=profit_overheads)
	    print(rate)
	    return JsonResponse(rate)