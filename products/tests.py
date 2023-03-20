from rest_framework.test import APITestCase
from rest_framework import status, request, response
from django.urls import reverse

from .models import *

class InitProductData:
    def __init__(self):
        brand = Brand.objects.create(title='Brando')
        for i in range(1, 11):
            Product.objects.create(
                title=f'Brando {i}',
                price=100,
                old_price=110,
                quantity=5,
                brand=brand,
                description='some description'
            )
class InitNewProductData:
    def __init__(self):
        brand = Brand.objects.create(title='BrandNew')
        product = Product.objects.create(
            title='BrandNew Something',
            price=999.99,
            old_price=1001,
            quantity= 2,
            brand=brand,
            description='very stylish and useful thing'
        )
        review = ProductReview.objects.create(
            review='',
            product=product
        )            


class ProductListTest(APITestCase):
    def test_product(self):
        url = reverse('list_of_products')
        self.maxDiff = None
        InitProductData()
        data = {
                "links": {
                    "next": "http://testserver/api/product/all/?page=2",
                    "previous": None,
                    "next_num_page": 2,
                    "previous_num_page": None
                },
                "page": 1,
                "pages": 5,
                "count": 10,
                "result": [
                    {
                        "id": 1,
                        "title": "Brando 1",
                        "price": "100.00",
                        "old_price": "110.00",
                        "quantity": 5,
                        "brand": {
                            "id": 1,
                            "title": "Brando"
                        }
                    },
                    {
                        "id": 2,
                        "title": "Brando 2",
                        "price": "100.00",
                        "old_price": "110.00",
                        "quantity": 5,
                        "brand": {
                            "id": 1,
                            "title": "Brando"
                        }
                    },
                   
                ]
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(Product.objects.count(), 2)


class ProductFilters(APITestCase): 
    #searching product by title test  
    def test_product_filterBy_title(self):
        url = reverse('list_of_products')
        InitProductData()
        search_title = "Brando 1"
        params = dict(
            title=search_title
        )
        response = self.client.get(url, params=params)
        print("found product by  brand and title!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['title'], search_title)
    #searching product by ID test
    def test_product_filterBy_id(self):
        url = reverse('list_of_products')
        InitProductData()
        search_id = 1
        params = dict(
            id=search_id
        )
        response = self.client.get(url, params=params)
        print("found product by ID!")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['id'], search_id)
    #searching product by max min price
    def test_product_filterBy_max_min_price(self):
        url = reverse('list_of_products')
        InitProductData()
        search_max_price= "{:.2f}".format(110)
        search_min_price =  "{:.2f}".format(100)
        params = dict(
           old_price=search_max_price,
           price= search_min_price
           )
        response = self.client.get(url, params=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['old_price'], search_max_price)
        self.assertEqual(response.data['result'][1]['price'], search_min_price)
    #searching product by brand ID
    def test_product_filterBy_brandId(self):
        url = reverse('list_of_products')
        InitProductData()
        search_brand_id = 1
        params = dict(
            brand=search_brand_id
            )
        response = self.client.get(url, params=params)
        print('found product by brand id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['brand']['id'], search_brand_id)

#creating new product with the new brand
class Createproduct(APITestCase):
    def test_create_product(self):
        brand = Brand.objects.create(title='BrandNew')
        review = ProductReview.objects.create(
            review='',
        )            
        InitNewProductData()
        requesting = {
            "title": "BrandNew Something",
            "price": 999.99,
            "old_price": 1001,
            "quantity": 1,
            "brand": brand.id,
            'description': 'very stylish and useful thing',
            'review': ['',]
        }
        url = reverse('create_product')
        data = {
            'title': 'BrandNew Something',
            'price': '999.99',
            'old_price': '1001',
            'description': 'very stylish and useful thing',
            'quantity': 1,
            'brand': 'BrandNew',
            'reviews': ['',]
        }
        response = self.client.post(url, data=requesting)
        print("new product created")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class NewProductActions(APITestCase):
    #updating product
    def test_update_product(self):
        InitNewProductData()
        requesting = {
            'price': 1200,
            'title': 'BrandNew Lux Item'
        }
        url = reverse('update_product', args=[1])
        data = {
            'title': 'BrandNew Lux Item',
            'price': '1200.00',
            'old_price': '1001',
            'description': 'very stylish and useful thing',
            'quantity': 1,
            'brand': 'BrandNew',
            'reviews': ['',]
        }
        response = self.client.patch(url, data=requesting)
        print("Updated")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #deleting product    
    def test_delete_product(self):
        InitNewProductData()
        url = reverse('product_find_delete', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



       
       


        
        
               
            
        



   
        
            
        



        
  
    


