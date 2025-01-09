from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView, AddOrderItemView, RemoveOrderItemView, UpdateOrderItemView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('orders/<int:order_id>/items/add/', AddOrderItemView.as_view(), name='add-order-item'),
    path('orders/items/<int:pk>/remove/', RemoveOrderItemView.as_view(), name='remove-order-item'),
    path('orders/items/<int:pk>/update/', UpdateOrderItemView.as_view(), name='update-order-item'),
]