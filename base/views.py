from django.shortcuts import render
from .models import ProductType, Department, Product, Sell, Purchase, Rating
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .serializers import ProductTypeSerializer, DepartmentSerializer, UserSerializer, LoginSerializer, ProductSerializer,SellSerializer, PurchaseSerializer, RatingSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Sum,Avg

# Create your views here.
class ProductTypeApiView(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductApiView(ModelViewSet):
    # queryset = Product.objects.all().order_by('-stock') ordering product datas in query according to stock in descending format using(-) removing (-) will give us product ordering according to stock in ascending format
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def best_selling(self,request):
        queryset = Product.objects.all().annotate(total_sell_quantity=Sum('sells__quantity')).order_by('-total_sell_quantity')
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    def most_purchased(self,request):
        queryset = Product.objects.all().annotate(total_purchased_quantity=Sum('purchases__quantity')).order_by('-total_purchased_quantity')
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    def top_rated(self,request):
        queryset = Product.objects.all().annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)


class SellApiView(ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer

class PurchaseApiView(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class RatingApiView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ProductTypeApiView(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class DepartmentApiView(GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk):
        # try:
        #     queryset = Department.objects.get(id=pk)
        # except:
        #     return Response({'error':'No matching data found!'}) # By default dictionary is converted onto json by Response class
        
        queryset = self.get_object()

        serializer = self.get_serializer(queryset,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def partial_update(self,request,pk):
        queryset = self.get_object()

        serializer = self.get_serializer(queryset,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def retrieve(self,request,pk):
        queryset = self.get_object()

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
    
    def destroy(self,request,pk):
        queryset = self.get_object()
        queryset.delete()
        return Response()

class UserApiView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def register(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def login(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(): # Validate whether user information is being sent or not
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username,password=password) # Passing username and password in authenticate to check whether it matches with any user or not, if matched it returns user object data if not it returns None

            if user == None: # If authenticate returned None, responding with invalid credentials response
                return Response({'error':'Invalid credentials!'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                token,_ = Token.objects.get_or_create(user=user) # Creating token object with user value , using get or create query because token object has user as one to one relation so we cannot create multiple token objects for a user 
                return Response({'token':token.key})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)