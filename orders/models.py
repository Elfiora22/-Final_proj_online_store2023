from django.db import models
from products.models import Product
from customers.models import Customer


class Order(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_checkout = models.DateTimeField(null=True, blank=True)
    time_delivery = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    customer_shipping_address = models.ForeignKey('customers.CustomerAddress', null=True, blank=True, on_delete=models.SET_NULL)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return str(self.customer)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2 )
    quantity = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = 'orders_products'
        verbose_name = 'Order product'
        verbose_name_plural = 'Orders products'

    def __str__(self):
        return self.product






