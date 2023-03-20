
from rest_framework import generics
from .serializers import  UserSerializer, CustomerSerializer, MyOrderdSerializer, UserTokenObtaiPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from orders.models import Order
from rest_framework.views import APIView
import uuid
from .models import Customer 
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.response import Response
from rest_framework import status


class UserCreate(APIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {
                'error': 'Both username and password are required.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        user = User.objects.create_user(username=username, password=password)
        if user:
            return Response(
                {
                'success': 'User created successfully.'
                },
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {
                'error': 'Failed to create user.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    

class CustomerCreate(APIView):
    http_method_names = ['post',]
    def post(self, *args, **kwargs):
        client_ip = self.request.META.get("REMOTE_ADDR")
        client_agent = self.request.META.get("HTTP_USER_AGENT")
        print("IP:", client_ip)
        print("AGENT:", client_agent)
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        response = {
            "status": True,
            "customer_token": customer_token,
            }
        return Response(data=response, status=status.HTTP_201_CREATED)



class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtaiPairSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegistration(APIView):
    authentication_classes = (JWTAuthentication, )#PROCEEDING REGISTRATION WITH AUTHENTICATED USER
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post',]
    def post_registration(self, *args, **kwargs):
        try:
            token = Customer.objects.get(token=self.request.data['token'])    
            username = Customer.objects.get_or_create(username=self.request.user['username'])
            first_name = Customer.objects.get_or_create(first_name=self.request.data['first_name'])
            last_name = Customer.objects.get_or_create(last_name=self.request.data['last_name'])
            email = Customer.objects.get_or_create(email=self.request.data['email'])
            password = Customer.objects.get_or_create(password=self.request.user['password'])
            response = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'token': token
                }
            return Response(data=response, status=status.HTTP_200_OK) 
        except Customer.DoesNotExist:
                response = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


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
    







    


