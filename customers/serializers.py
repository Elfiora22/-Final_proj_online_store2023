from rest_framework import serializers
from .models import Customer
from orders.models import Order


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = "__all__"


class MyOrderdSerializer(serializers.ModelSerializer):

    class Meta:
        model= Order
        fields = "__all__"