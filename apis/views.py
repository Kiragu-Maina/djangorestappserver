from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rates.utils import utility
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProductsSerializer, ProductSerializer, ShopSerializer
from .models import Products, Product, Shop


class ProductListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

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
            request.session['logged_in_user'] = username
            token, _ = Token.objects.get_or_create(user=user)

            # Include the token in the response data
            return Response({'token': token.key, 'message': 'Logged in successfully.'})
        
            
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
class CategoriesView(APIView):
    authentication_classes = []
    permission_classes = []
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        categories = [
                'Hand Tools',
                'Power Tools',
                'Fasteners',
                'Building Materials',
                'Paint and Finishing Supplies',
                'Plumbing Supplies',
                'Electrical Supplies',
                'Safety and Protective Gear',
                'Hardware Accessories',
                'Gardening and Outdoor Supplies'
            ]

        
        return Response(categories)



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

        data_list = request.data
        print(data_list)  # Assuming request.data is a list of dictionaries
        username = self.kwargs.get('username', None)

        # shop_name = request.session.get('shop_name')
        shop = Shop.objects.filter(shop_owner=username).first()

  # Assign the Shop object's ID to the 'shop' field
        context = {'shop_id': shop.id}  # Provide the shop_id in the context
        for data in data_list:
            serializer = ProductSerializer(data=data, context=context)

            
            print(serializer)
            if serializer.is_valid():
                serializer.save()  # Create and save the product objects
                
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Products created successfully.'}, status=status.HTTP_201_CREATED)


class ProductsView(APIView):
    authentication_classes = []
    permission_classes = []
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, request):
        print(request)
        username = self.kwargs.get('username', None)
        if username != 'none':

       
            shop_name = Shop.objects.filter(shop_owner=username).values_list('shopname', flat=True).first()
            request.session['shop_name'] = shop_name
            print('shopname in productsview is: ', shop_name)

            if shop_name is not None:
                # Do something with the shop_name
                print(f"The shop name in session is: {shop_name}")
                queryset = Product.objects.filter(shop__shopname=shop_name)
                print(queryset)
            else:
                # Handle the case when the shop_name is not found in the session
                queryset = Product.objects.all()
        else:
            queryset = Product.objects.all()

     
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class CreateShop(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            shop = serializer.save()  # Create and save the shop object
            # Additional logic or response handling
            return JsonResponse(serializer.data, status=200)
        else:
            errors = serializer.errors
            return JsonResponse(errors, status=400)
        

class CheckShop(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        username = kwargs['username']  # Assuming 'username' is part of the URL path parameter
        # Handle the 'GET' request logic here
        # Example: Retrieve data or perform any necessary operations
        # You can use the 'username' to fetch the corresponding data from the database
        # Replace 'Shop.objects.get()' with the appropriate query to retrieve the shop_owner based on 'username'
        try:
            exists = Shop.objects.filter(shop_owner=username).exists()

            if exists:
                print('exists')
                try:
                    shop_name = Shop.objects.filter(shop_owner=username).values_list('shopname', flat=True).first()

                    if shop_name is not None:
                        # Do something with the shop_name
                        print(f"The shop name in session is: {shop_name}")
                        request.session['shop_name'] = shop_name
                        request.session.save()
                    else:
                        
                        # Handle the case when the shop_name is not found in the session
                        print("Shop name not found for the given username.")
                except Exception as e:
                    print(f"Error occurred during database query: {e}")
                
            return JsonResponse({'exists': exists}, status=200)
        except:
            return JsonResponse({'exists': False}, status=400)  

      


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
       
        return super().dispatch(request, *args, **kwargs)
    

