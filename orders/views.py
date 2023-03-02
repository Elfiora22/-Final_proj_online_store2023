
from rest_framework.views import APIView
from orders.models import OrderProduct, Order
from products.models import Product
from customers.models import Customer, CustomerAddress
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics
from uuid import *
from .serializers import OrderProductSerializer, OrderSerializer

class UpdateCart(APIView):
    http_method_names = ['post',]
    def post(self, *args, **kwargs):
        try:
            try:
                customer = Customer.objects.get(token=self.request.data['token'])#GET CUSTOMER BY TOKEN iF EXISTS
            except Customer.DoesNotExist:
                responce = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(pk=self.request.data['product_id'])#GET PRODUCT BY ID IF EXISTS
            except Product.DoesNotExist:
                responce = {
                    'status': False,
                    'error': 'Product does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST) 

            if product.quantity < self.request.data['quantity']:
                responce ={
                    'status': False,
                    'error': 'Last item left'#DEFAULT QUANTITY==1, NOT NULL, NOT BLANK
                }
                return  Response(data=responce, status=status.HTTP_400_BAD_REQUEST)

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
            responce = {
                'status': True,
                'cart_items_count': count_items    
            }# RESPONCE FOR CART UPDATE!

            product.quantity = product.quantity - self.request.data['quantity']#QUANTITY OF PRODUCTS LEFT AFTER THIS ORDER
            product.save()

            return Response(data=responce, status=status.HTTP_200_OK) 
         
        except BaseException as error:
            responce ={
                'status': False,
                'error': str(error)
            } 
            return Response(data=responce, status=status.HTTP_200_OK)


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
    serializer_class= OrderSerializer#хочется знать, уместен ли тут это?
    queryset = Order.objects.all() 
    http_method_names = ['put',]
    def finalize_order_set(self, request, *args, **kwargs):
        try:
            try: #Retrieving a customer_order and order__customer__token  ????нам ведь нужен именно покупатель, у которого есть товар в корзине, так? 
                customer = OrderProduct.objects.get(
                    order__customer=self.request.data['order__customer'],
                    order__is_ordered=False
                    )
                token = OrderProduct.objects.get(
                    order__customer__token=self.request.data['order__customer__token'], 
                    order__is_ordered=False
                    )
            except customer is None:
                responce = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)

            try:
                #Checking unfinished  orders (when is_ordered=False) for the customer 
                order = OrderProduct.objects.get(
                    order_product__order =self.request.data['order'], 
                    order_customer=customer, 
                    order_is_ordered=False
                    )
            except order is None:
                responce = {
                    'status': False,
                    'error': 'Customer has no active orders at the moment'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)
            try:
            #Rertrieving customer data - Customer  Model
                customer.first_name = Customer.objects.get_or_create(first_name=self.request.data['first_name'])
                customer.last_name = Customer.objects.get_or_create(last_name=self.request.data['last_name'])
                customer.email = Customer.objects.get_or_create(email=self.request.data['email'])
                customer.phone = Customer.objects.get_or_create(phone=self.request.data['phone'])
                customer.address = Customer.objects.get_or_create(address=self.request.data['address'])
                customer.save()
            except Customer.DoesNotExist:
                responce ={
                'status': False,
                'error': 'Customer does not exist'
                } 
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)
                    
            try:
                ##Rertrieving CustomerAddress data - CustomerAddress Model
                customer.address_city = CustomerAddress.objects.get_or_create(city=self.request.data['city'], customer=customer)
                customer.address_post_code = CustomerAddress.objects.get_or_create(post_code=self.request.data['post_code'], customer=customer)
                customer.address_country = CustomerAddress.objects.get_or_create(country=self.request.data['country'], customer=customer)
                customer = CustomerAddress.objects.get_or_create(customer=self.request.data['customer'])
                customer.address_address =CustomerAddress.objects.get_or_create(customer_address=self.request.data['customer_address'], customer=customer)
                customer.customer_address.save()
            except CustomerAddress.DoesNotExist:
                responce ={
                'status': False,
                'error': 'Customer does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)        
            request = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'post_code': customer.address_post_code,
                'phone': customer.phone,
                'country': customer.address_country,
                'city': customer.address_city,
                'address': customer.address_address,
                'token': token
                }       
            order_serializer = self.serializer_class(data=request.data)
            if order_serializer.is_valid():
                #Processing validated data here and saving: ???? так можно?
                time_created = order_serializer.validated_data['time_created']
                time_checkout = order_serializer.validated_data['time_checkout']
                time_delivery = order_serializer._validated_data['time_delivery']
                customer = order_serializer.validated_data['customer']
                customer_shipping_address= order_serializer.validated_data['customer_shipping_address']
                is_ordered = order_serializer.validated_data['True']
                order_serializer.save()
            #Formatting final responce:
            responce = {
                'id': order,
                'time-created': time_created,
                'time_checkout': time_checkout,
                'time_delivery': time_delivery,
                'is_ordered': is_ordered,
                'customer': customer,
                'customer_shipping_address': customer_shipping_address    
                }
            return Response(data=responce, status=status.HTTP_200_OK)
        except BaseException as error:
            responce ={
            'status': False,
            'error': 'No customer matching this order'
            }
            return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)
            





            




   
        





  

