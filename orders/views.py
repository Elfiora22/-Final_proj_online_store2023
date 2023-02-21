
from rest_framework.views import APIView
from orders.models import OrderProduct, Order
from products.models import Product
from customers.models import Customer
from rest_framework.response import Response
from rest_framework import status


class UpdateCart(APIView):
    http_method_names = ['post',]
    def post(self, *args, **kwargs):
        try:
            try:
                customer = Customer.objects.get(token=self.request.data['token'])#GET CUSTOMER BY TOKEN
            except Customer.DoesNotExist:
                responce = {
                    'status': False,
                    'error': 'Customer does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(pk=self.request.data['product_id'])#GET PRODUCT BY ID
                product_quantity = Product.objects.get(quantity=self.request.data['quantity'])#GET QUANTITY OF CERTAIN PRODUCT
                if product_quantity <= 2:
                    responce ={
                        'status': False,
                        'error': 'Last item left'#DEFAULT QUANTITY==1, NOT NULL, NOT BLANK
                    }
            except Product.DoesNotExist:
                responce = {
                    'status': False,
                    'error': 'Product does not exist'
                }
                return Response(data=responce, status=status.HTTP_400_BAD_REQUEST) 


            orders = Order.objects.filter(customer=customer, is_ordered=False).order_by('-id')#also  could be filtered by "-time_created" (DESC)
            if orders.count() == 0:
                order = Order.objects.create(customer=customer)
            else:
                order = orders[0]#ONLY ONE PRODUCT IN THE ORDER

            try:
                product_order = OrderProduct.objects.get(order=order, product=product)
                if self.request.data['quantity'] == 0:
                    product_order.delete()# DELETING PRODUCT FROM ORDER
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
            }
            return Response(data=responce, status=status.HTTP_200_OK) 
         
        except BaseException as error:
            responce ={
                'status': False,
                'error': str(error)
            } 
            return Response(data=responce, status=status.HTTP_400_BAD_REQUEST)    
            




  

