import json
from json import loads
import uuid
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from customers.models import *
from .models import *
from products.models import *
from products.tests import *

from products.tests import InitProductData

class CartTestCase(APITestCase):
    def test_update_cart(self):    
        customer_token = str(uuid.uuid4())
        Customer.objects.create(token=customer_token)
        InitProductData()         
        url = reverse('update_cart')
        requesting = {
            "product_id": 2,
            "quantity": 1,
            "token": customer_token
        }
        data = {
            "status": True,
            "cart_items_count": 1
         }
        response = self.client.post(url, data=requesting)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    