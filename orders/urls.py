from django.urls import path
from .views import *


urlpatterns = [
    path('cart/update/', UpdateCart.as_view(), name='update_cart'),
    path('cart/list/<slug:token>/', CartList.as_view(), name="get_cart_list"),
    path('finalize/', FinalizeOrder.as_view(), name="finalize_order")

   
]


