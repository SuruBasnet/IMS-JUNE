from django.shortcuts import render
from .models import ProductType, Department
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .serializers import ProductTypeSerializer, DepartmentSerializer
from rest_framework import status

# Create your views here.
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
        
