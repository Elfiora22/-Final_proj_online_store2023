from django.http.response import HttpResponse
from rest_framework import generics
from .serializers import CustomerSerializer, MyOrderdSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from rest_framework.views import APIView
import uuid
from .models import Customer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class CustomerCreate(APIView):
    http_method_names = ['post',]
    def post(self, *args, **kwargs):
        client_ip = self.request.META.get("REMOTE_ADDR")
        client_agent = self.request.META.get("HTTP_USER_AGENT")
        print("IP:", client_ip)
        print("AGENT:", client_agent)
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        responce = {
            "status": True,
            "customer_token": customer_token,
            }
        return Response(status=HTTP_201_CREATED, data=responce)   


class GetAuthCustomer(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer



class MyOrders(generics.ListAPIView):
    serializer_class = MyOrderdSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.filter(customer__user = self.request.user)
    







    


