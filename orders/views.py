
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
    http_method_names = ['put',]
    serializer_class = OrderSerializer#??? сериалайзер использовала в качестве эксперимента
    queryset = Order.objects.all()

    def finalize_order_set(self, request, *args, **kwargs):
        try:
            try: #Retrieving a customer'token, if not, creating a new one ?? надо?
                customer = Customer.objects.get(token=self.request.data['token'])
                if customer.token is None:
                    customer_token = str(uuid4())# ??? здесь нужна эта переменная? или ситуации, когда нет токена -просто не может быть?
                    customer.token = Customer.objects.create(token=customer_token)
            except Customer.DoesNotExist:
                responce = {
                    'status': False,
                    'error': 'Customer does not exist'# по шаблону  CartUpdate
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)

            try:
                #Checking unfinished  orders (when is_ordered=False) for the customer
                orders = Order.objects.filter(customer=customer, is_ordered=False).order_by['-id']#  тоже по шаблону  CartUpdate
                if orders.count() == 0:
                    order = Order.objects.create(customer=customer)
                else:
                    order = orders[0]
            except order is None:
                responce = {
                    'status': False,
                    'error': 'Customer has no active orders at the moment'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)
            try:
            #Rertrieving customers data
                customer.first_name = self.request.data.get('first_name', customer.first_name)
                customer.last_name = self.request.get('last_name', customer.last_name)
                customer.email = self.request.data.get('email', customer.email)
                customer.phone = self.request.data.get('phone', customer.phone)
                customer.address = self.request.data.get('address', customer.address)
                customer.token = self.request.data.get('token', customer.token)
                customer.save()
            except Customer.DoesNotExist:#if not exist, creating a customer (all fields of the Customer Model)
                customer = Customer.objects.create(
                    first_name= customer.first_name,
                    last_name= customer.last_name,
                    email=customer.email,
                    phone=customer.phone,
                    time_created=customer.time_created,
                    address=customer.address,
                    token=customer.token,
                    user=customer.user
                )           
            try:
                ##Rertrieving CustomerAddress data
                customer_address = CustomerAddress.objects.get(customer=customer)
                customer_address.city = self.request.data['city']
                customer_address.post_code = self.request.data['post_code']
                customer_address.country = self.request.data['country']
                customer_address.address = self.request.data['address']# oбратный адрес покупателя
                customer_address.customer = self.request.data['customer']
                customer_address.save()
            except CustomerAddress.DoesNotExist:##if not exist, creating a customer (all fields of the CustomerAddress Model)
                customer_address = CustomerAddress.objects.create(
                    city=customer_address.city,
                    post_code=customer_address.post_code,
                    country=customer_address.country,
                    address= customer_address.address,
                    customer=customer_address.customer,
                )
            request = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'post_code': customer_address.post_code,
                'phone': customer.phone,
                'country': customer_address.country,
                'city': customer_address.city,
                'address': customer.address,
                'token': customer.token
                }       
            order_serializer = self.serializer_class(data=request.data)
            if order_serializer.is_valid():
            #Processing validated data here and saving: ???? так нормально?
                time_created = order_serializer.validated_data['time_created']
                time_checkout = order_serializer.validated_data['time_checkout']
                time_delivery = order_serializer._validated_data['time_delivery']
                customer = order_serializer.validated_data['customer-id']
                customer_shipping_address= order_serializer._validated_data['customer_shipping_address']
                is_ordered = order_serializer._validated_data['True']
                order_serializer.save()
                #Formatting final responce:
            responce = {
                'status': True,
                'id': order,
                'time-created': time_created,
                'time_checkout': time_checkout,
                'time_delivery': time_delivery,
                'is_ordered': is_ordered,
                'customer': customer,
                'customer_shipping_address': customer_shipping_address    
                }
            return Response(data=responce, status=status.HTTP_200_OK) 
        except BaseException as message:
            responce ={
                'status': False,
                'message': 'everything went wrong = все пропало!'#hope NO!
                }
            return Response(data=responce, status=status.HTTP_400_BAD_REQUEST) 
            






          

        
       



            




   
        





  

