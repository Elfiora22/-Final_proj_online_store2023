from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Last Name")
    phone = models.BigIntegerField(unique=True, null=True, blank =True)
    email = models.CharField(max_length=200, blank=True, null=True, verbose_name="Email")
    time_created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    token = models.CharField(max_length=300, null=False, blank=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.last_name


class CustomerAddress(models.Model):
    city = models.CharField(max_length=50, blank=False, null=False, verbose_name='City')
    post_code = models.IntegerField(blank=False, null=False, verbose_name='Post Code')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Country')
    address = models.CharField(max_length= 200, default='', blank=False, null=False, verbose_name='Street-address')
    customer = models.ForeignKey("customers.Customer", blank=False, null=False, on_delete=models.CASCADE, verbose_name='Customer')

    class Meta:
        db_table = 'customer_addresses'
        verbose_name = 'Customer address'
        verbose_name_plural = 'Customers addresses'

    def __str__(self):
        return self.address









