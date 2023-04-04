
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CustomerCreate(APIView):
    http_method_names = ['post']
    def post(self, *args, **qargs):
        client_ip = self.request.META.get('REMOTE_ADDR')
        client_agent = self.request.META.get('HTTP_USER_AGENT')
        print('IP:', client_ip)
        print('client agent:', client_agent)

        customer_token = str(uuid.uuid4())
        customer =Customer.objects.create(token=customer_token)
        response = {
                'status': True,
                'customer_token': customer_token,
            }
        return Response(data=response, status= status.HTTP_201_CREATED)


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


class UserCreateRegistration(APIView):
    authentication_classes = (JWTAuthentication, )#PROCEEDING REGISTRATION WITH AUTHENTICATED USER
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post',]
    def post_registration(self, *args, **kwargs):
        try:
            token = Customer.objects.create(token=str(uuid.uuid4()))    
            username = User.objects.create_user(username=self.username)
            first_name = Customer.objects.create(first_name=self.first_name)
            last_name = Customer.objects.create(last_name=self.last_name)
            email = Customer.objects.create(email=self.email)
            password = User.objects.create_user(password=self.password)
            response = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'token': token
            }
        except BaseException as error:
            response ={
                'status': False,
                'error': str(error)
            } 
            return Response(data=response, status=status.HTTP_200_OK)


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
    







    


