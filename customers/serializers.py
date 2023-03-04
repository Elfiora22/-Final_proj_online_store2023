from rest_framework import serializers
from .models import Customer
from orders.models import Order
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
User = get_user_model


class UserTokenObtaiPairSerializer(TokenObtainPairSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class  UserTokenRefreshSerializer(TokenRefreshSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']       

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = "__all__"
        


class MyOrderdSerializer(serializers.ModelSerializer):

    class Meta:
        model= Order
        fields = "__all__"