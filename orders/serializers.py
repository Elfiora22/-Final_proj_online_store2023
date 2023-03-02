from rest_framework import serializers
from .models import OrderProduct, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order,
        fields = "__all__"

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = "__all__"