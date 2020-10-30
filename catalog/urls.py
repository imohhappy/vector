from . import views
from django.urls import path
from.views import (
    product_detail, CategoryDetail, CategoryView, cart_add, cart_detail, cart_remove, order_create
)


app_name = 'product'

urlpatterns = [
    path('', CategoryView.as_view(), name='vacancy'),
    path('cart/', cart_detail, name='cart_detail'),
    path('<int:pk>/', CategoryDetail.as_view(), name='detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('create/', order_create, name='order_create'),
    path('<int:category_id>/<slug:slug>/', product_detail, name='cloth'),
]
