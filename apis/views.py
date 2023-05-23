from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rates.models import Shop, Inventory
from rates.utils import utility
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import AbstractProducts

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            User.objects.create_user(username=username, email=email, password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Logged in successfully.'})
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


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

class ProductsUpload(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data'))

        # Extract the relevant data from the request
        item_name = data.get('itemName')
        description = data.get('description')
        price = data.get('price')
        quantity = data.get('quantity')

        # Get the uploaded image file
        image_file = request.FILES.get('image')

        # Create a new instance of AbstractProducts and save the data
        product = AbstractProducts(
            itemName=item_name,
            description=description,
            price=price,
            quantity=quantity,
            image=image_file
        )
        product.save()

        return JsonResponse({'message': 'Product created successfully.'}, status=201)
