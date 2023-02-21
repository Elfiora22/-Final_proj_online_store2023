from django.urls import path
from .views import *


urlpatterns =[
    path('myorders/', MyOrders.as_view()),
    path('create/', CustomerCreate.as_view()),

]