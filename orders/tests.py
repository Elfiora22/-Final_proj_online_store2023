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
from django.utils import timezone


class CartTestCase(APITestCase):
    def test_update_cart(self):
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token) 
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

    def test_get_cart_list(self):
        customer_token = str(uuid.uuid4())
        customer = Customer.objects.create(token=customer_token)
        customer_address = CustomerAddress.objects.create(
            city= "New York",
            post_code= 10001-2866,
            country= "USA",
            address = "171 Bowery",
            customer= customer    
        )
        order = Order.objects.create(
            customer=customer,     
            is_ordered = False,
            customer_shipping_address= customer_address  
            )
        product = Product.objects.create()
        # creating a new order-product relation
        OrderProduct.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=2
        )
        data = [
            {
                'id': 1,
                'price': '100.00',
                'quantity': 2,
                'product': 2,
                'order': 1,
            },
        ]
        url = reverse('get_cart_list', kwargs={'token': customer.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FinalizeOrderTest(APITestCase):
    def test_finalize_order(self):
        def set_all(self):
            #customer token 
            customer_token = str(uuid.uuid4())
            url = reverse('customer_create')
            request = self.client.post(url)
            response = {
                'status': True,
                'customer_token': customer_token
            }
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            #customer details
            customer = Customer.objects.create(
                token= customer_token,
                email= "testuser334@dd.com",
                first_name= "Nicki",
                last_name= "Caraways",
                phone= 7633444,
            )
            #customer address for the order  
            customer_address = CustomerAddress.objects.create(
                city= "New York",
                post_code= 10001,
                country= "USA",
                address = "188 Bowery",
                customer= customer 
            )
            #order itserlf
            order = Order.objects.create(
                customer=customer,     
                is_ordered = False,
                customer_shipping_address= customer_address
            )
            #product
            product = Product.objects.create()
            #cart aka order_product    
            order_product = OrderProduct.objects.create(
                price = 100,
                quantity=1,
                order= order,
                product_id= product.id
            )
            #Finalizing request
            request_data = {
                "first_name": "Nicki",
                "last_name": "Caraways",
                "email": "testuser334@dd.com",
                "post_code": 10001,
                "phone": 7633444,
                "country": "USA",
                "city": "New York",
                "address": "188 Bowery",
                "token": customer_token
            }
            #Setting response
            response_data = {
                "id": order.id,
                "time_created": timezone.now(),
                "time_checkout": timezone.now(),
                "time_delivery": None,
                "is_ordered": True,
                "customer": customer,
                "customer_shipping_address": customer_address
            }
            url = reverse('finalize_order')
            response = self.client.put(url, request_data, format='json')
            #needing more asserts
            self.assertEqual(response.status_code,  status.HTTP_200_OK)    







        





         

    



        
    
    