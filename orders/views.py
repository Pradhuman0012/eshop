from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from drf_yasg.utils import swagger_auto_schema

class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={
            201: "Order created successfully",
            400: "Invalid data",
        }
    )
    def post(self, request):
        items_data = request.data.pop('items', [])
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            for item in items_data:
                product_id = item.get('product')
                quantity = item.get('quantity')
                price = item.get('price')
                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    quantity=quantity,
                    price=price,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=OrderItemSerializer,
        responses={
            201: "Item added successfully",
            400: "Invalid data",
        }
    )
    def post(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, user=request.user, status="Pending")
        except Order.DoesNotExist:
            return Response({"error": "Order not found or cannot add items to this order."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            order_item = OrderItem.objects.get(pk=pk, order__user=request.user, order__status="Pending")
        except OrderItem.DoesNotExist:
            return Response({"error": "Order item not found or cannot be removed."}, status=status.HTTP_404_NOT_FOUND)

        order_item.delete()
        return Response({"message": "Order item removed successfully."}, status=status.HTTP_204_NO_CONTENT)


class UpdateOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=OrderItemSerializer,
        responses={
            200: "Item updated successfully",
            400: "Invalid data",
        }
    )
    def put(self, request, pk):
        try:
            order_item = OrderItem.objects.get(pk=pk, order__user=request.user, order__status="Pending")
        except OrderItem.DoesNotExist:
            return Response({"error": "Order item not found or cannot be updated."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)