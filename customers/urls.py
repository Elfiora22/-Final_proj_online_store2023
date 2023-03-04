from django.urls import path
from .views import *


urlpatterns =[
    path('myorders/', MyOrders.as_view(), name='my_orders'),
    path('create/', CustomerCreate.as_view(), name='customer_create'),
    path('registration/', CustomerRegistration.as_view(),name='registration'),
]