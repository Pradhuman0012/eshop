from django.shortcuts import render
from .models import Product
from rest_framework.views import APIView
from rest_framework import status,permissions
from .serializers import ProductSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class ProductListView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request):
        product=Product.objects.all()
        serializer=ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self,request,pk):
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error":"Product does not exist"},status=status.HTTP_404_NOT_FOUND)
        serializer= ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductCreateView(APIView):
    permission_classes=[permissions.IsAdminUser]
    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,  # This adds the payload description
        responses={
            201: ProductSerializer,  # Successful creation response
            400: 'Bad Request'  # In case of invalid request
        }
    )
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    permission_classes=[permissions.IsAdminUser]
    def delete(self,request,pk):
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error":"product not found"},status=status.HTTP_204_NO_CONTENT)
        product.delete()
        return Response({"success":"product deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    

class ProductUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)