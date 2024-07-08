from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductsListView,
    ProductDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrdersListView,
    OrdersDetailView,
    OrderCreateView,
    OrdersUpdateView,
    OrderDeleteView,
    ProductDataExportView,
    ProductViewSet,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/export/', ProductDataExportView.as_view(), name='product-export'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>update/', OrdersUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>confirm-delete/', OrderDeleteView.as_view(), name='order_delete'),
]
