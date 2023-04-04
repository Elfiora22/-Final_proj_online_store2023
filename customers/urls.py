from django.urls import path
from .views import *


urlpatterns =[
    path('myorders/', MyOrders.as_view(), name='my_orders'),
    path('create/', CustomerCreate.as_view(), name='customer_create'),
    path('jwt/auth/', UserTokenObtainPairView.as_view(), name='obtain_pair'),
    path('registration/', UserCreateRegistration.as_view(),name='registration'),
    path("getuser/", GetAuthCustomer.as_view(), name='get_user'),
]