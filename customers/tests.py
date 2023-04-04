import json
import uuid
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from customers.models import *
from orders.models import Order
User = get_user_model()

#user creation and auth
class UserAuthorizationTestCase(APITestCase):
    #create a new user 
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='tesstuser',
            password='Nothanks2'
        )
    #login user
    def test_user_authorization(self, *args, **kwargs):
        # Log in the user
        response = self.client.post(reverse('token_obtain_pair'), 
            {
            'username': 'tesstuser', 
            'password': 'Nothanks2'
            })
        print("New user logged in!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Extract the access token from the response
        access_token = response.data['access']
        print(f"Here is user's Acess Token {access_token}")
        # Add the token to the authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # Log out the user
        self.client.credentials(HTTP_AUTHORIZATION='')


#creatinh a customer
class CustomerTestCase(APITestCase):
    authentication_classes = (JWTAuthentication, )#PROCEEDING REGISTRATION WITH AUTHENTICATED USER
    def test_customer_create(self):
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        url = reverse('customer_create')
        request_data = {
            'token': customer_token,
        }
        data = {
            'status': True,
            'customer_token': customer_token
        }
        response = self.client.post(url, data=request_data, format='json')
        print("Customer created!")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CustomerUserRegistration(APITestCase):
    def test_user_registration(self):
        def user_authorization(self, *args, **kwargs):
        # Log in the user
            response = self.client.post(reverse('token_obtain_pair'), 
            {
                'username': 'tesstuser', 
                'password': 'Nothanks2'
            })
            print("User logged in!")
        # Extracting the access token from the response
            access_token = response.data['access']
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
            customer_token = str(uuid.uuid4())
            customer = Customer.objects.create(token=customer_token)
            self.assertIsNotNone(customer.token)
        # Creating a request for registration
            request_data = {
                'username': 'tesstuser',
                'email': 'testo@testo.com',
                'first_name': 'Jay',
                'last_name': 'Gatsby',
                'password': 'Nothanks2',
                'token': customer_token
            }
            url = reverse('registration')
            response = self.client.post(url, request_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # user was created
            self.assertTrue(User.objects.filter(username='tesstuser').exists())



            

        
        
    





        
