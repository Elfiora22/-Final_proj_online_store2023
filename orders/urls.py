from django.urls import path
from .views import *


urlpatterns =[
    path('cart/list/<token>/', UpdateCart.as_view()),
    
]


