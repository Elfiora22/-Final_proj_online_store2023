
from rest_framework import generics
from .serializers import CustomerSerializer, MyOrderdSerializer, UserTokenObtaiPairSerializer, UserTokenRefreshSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from rest_framework.views import APIView
import uuid
from .models import Customer 
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
User = get_user_model()

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
        return Response(data=responce, status=status.HTTP_201_CREATED)
    
"""
???? вот тут меня терзают смутные сомнения: у нас в  сore > urls.py написано 2 views: TokenObtainPairView и TokenRefreshView. А в
документации Postman их сразу два в responce.  Я тут, на всякий случай сделала 2 сериалайзера и 2view. Но что-то как-то
здесь не так... 
"""  

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtaiPairSerializer
    authentication_classes = (JWTAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        responce = {
            'access': str(JWTAuthentication.get_validated_token),
        } 
        return Response(data=responce, status=status.HTTP_201_CREATED)


class TokenRefreshView(TokenRefreshView):
    serializer_class = UserTokenRefreshSerializer
    authentication_classes = (JWTAuthentication)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        responce = {
            'access': str(JWTAuthentication.get_validated_token),
        } 
        return Response(data=responce, status=status.HTTP_201_CREATED)


class CustomerRegistration(APIView):
    authentication_classes = (JWTAuthentication, )#PROCEEDING REGISTRATION WITH AUTHENTICATED USER
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post',]
    def post_registration(self, *args, **kwargs):
        try:
            token = Customer.objects.get(token=self.request.data['token'])    
            username = Customer.objects.get(username=self.request.user['username'])
            first_name = Customer.objects.get_or_create(first_name=self.request.data['first_name'])
            last_name = Customer.objects.get_or_create(last_name=self.request.data['last_name'])
            email = Customer.objects.get_or_create(email=self.request.data['email'])
            password = Customer.objects.get(password=self.request.user['password'])
            responce = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'token': token
                }
            return Response(data=responce, status=status.HTTP_200_OK) 
        except Customer.DoesNotExist:
                responce = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)


class GetAuthCustomer(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        return Customer.objects.filter(customer__user=self.request.user)
    


class MyOrders(generics.ListAPIView):
    serializer_class = MyOrderdSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.filter(customer__user = self.request.user)
    







    


