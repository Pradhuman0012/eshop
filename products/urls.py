from django.urls import path
from products import views
urlpatterns = [
    path('product_list/', views.ProductListView.as_view(),name="product_list"),
    path('product_create', views.ProductCreateView.as_view(),name="product_create"),
    path('product_details/<int:pk>', views.ProductDetailView.as_view(),name="product_details"),
    path('product_update/<int:pk>', views.ProductUpdateView.as_view(),name="product_update"),
    path('product_delete/<int:pk>', views.ProductDeleteView.as_view(),name="product_delete"),
   
]