
from rest_framework.views import APIView
from orders.models import OrderProduct, Order
from products.models import Product
from customers.models import Customer, CustomerAddress
from rest_framework.response import Response
from rest_framework import status, generics
from uuid import *
from .serializers import OrderProductSerializer
from django.utils import timezone

class UpdateCart(APIView):
    http_method_names = ['post',]
    def post(self, *args, **kwargs):
        try:
            try:
                customer = Customer.objects.get(token=self.request.data['token'])#GET CUSTOMER BY TOKEN iF EXISTS
            except Customer.DoesNotExist:
                response = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(pk=self.request.data['product_id'])#GET PRODUCT BY ID IF EXISTS
            except Product.DoesNotExist:
                response = {
                    'status': False,
                    'error': 'Product does not exist'
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST) 

            if product.quantity < self.request.data['quantity']:
                response ={
                    'status': False,
                    'error': 'Last item left'#DEFAULT QUANTITY==1, NOT NULL, NOT BLANK
                }
                return  Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            orders = Order.objects.filter(customer=customer, is_ordered=False).order_by('-id')#also  could be filtered by "-time_created" (DESC)
            if orders.count() == 0:
                order = Order.objects.create(customer=customer)
            else:
                order = orders[0]#SHOW ONLY/LAST ORDER

            try:
                product_order = OrderProduct.objects.get(order=order, product=product)
                if self.request.data['quantity'] == 0:
                    product_order.delete()# DELETING PRODUCT FROM ORDER IF QUANTITY NOT STATED
                else:
                    product_order.quantity = self.request.data['quantity']#  SETTING FOR "UPDATE CART" RESPONSE 
                    product_order.price = product.price
                    product_order.save()
            except OrderProduct.DoesNotExist:
                OrderProduct.objects.create(
                    order = order,
                    product = product,
                    price = product.price,
                    quantity = self.request.data['quantity']#CREATING CART IF NOT EXISTED  
                )
            products_in_order = OrderProduct.objects.filter(order=order)#COUNTING ITEMS IN THE CART
            count_items = 0
            for item in products_in_order:
                count_items += item['quantity']
            response = {
                'status': True,
                'cart_items_count': count_items    
            }# RESPONCE FOR CART UPDATE!

            product.quantity = product.quantity - self.request.data['quantity']#QUANTITY OF PRODUCTS LEFT AFTER THIS ORDER
            product.save()

            return Response(data=response, status=status.HTTP_200_OK) 
         
        except BaseException as error:
            response ={
                'status': False,
                'error': str(error)
            } 
            return Response(data=response, status=status.HTTP_200_OK)


class CartList(generics.ListAPIView):
    serializer_class = OrderProductSerializer
    def get_queryset(self):
        try:
            return OrderProduct.objects.filter(
              order__customer__token = self.kwargs["token"], 
              order__is_ordered=False  
            )
        except BaseException:
            return None
        

class FinalizeOrder(APIView):
    http_method_names = ['put',]
    def put(self, request, *args, **kwargs):
        try:  
            #Retrieving customer's token for cart 
            token = OrderProduct.objects.filter(
                order__customer__token = self.kwargs['token'],
                order__is_ordered=False     
            )
            #customer for cart
            customer = OrderProduct.objects.filter(
                order__customer = self.kwargs['customer'],
                order__is_ordered=False
            )    
            #Checking unfinished  orders in order_product (when is_ordered=False) for the customer 
            order = OrderProduct.objects.filter( 
                order = order,
                order__customer = customer,
                order__is_ordered=False
            )    
            #Rertrieving customer data
            first_name = Customer.objects.get_or_create(first_name=self.request.data['first_name'])
            last_name = Customer.objects.get_or_create(last_name=self.request.data['last_name'])
            email = Customer.objects.get_or_create(email=self.request.data['email'])
            phone = Customer.objects.get_or_create(phone=self.request.data['phone'])
            customer_shipping_address = Customer.objects.get_or_create(shipping_address= self.request.data['customer_shipping_address'])
            #Rertrieving CustomerAddress data using CustomerAddress Model and saving them
            address_city = CustomerAddress.objects.filter(city=self.request.data['city'], customer=customer)
            address_post_code = CustomerAddress.objects.filter(post_code=self.request.data['post_code'], customer=customer)
            address_country = CustomerAddress.objects.filter(country=self.request.data['country'], customer=customer)
            address_address =CustomerAddress.objects.filter(customer_address=self.request.data['customer_address'], customer=customer)
            request = {
                'first_name': first_name,
               'last_name': last_name,
                'email': email,
                'post_code': address_post_code,
                'phone': phone,
                'country': address_country,
                'city': address_city,
                'address': address_address,
                'token': token
                }       
            #Creating final responce:
            response = {
                'id': order,
                'time-created': timezone.now(),
                'time_checkout': timezone.now(),
                'time_delivery': None,
                'is_ordered': True,
                'customer': customer,
                'customer_shipping_address': customer_shipping_address  
                }
            return Response(data=response, status=status.HTTP_200_OK)
        except BaseException as error:
            response ={
            'status': False,
            'error': 'No customer matching this order'
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        