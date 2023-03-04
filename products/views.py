#from django.http.response import HttpResponse
from rest_framework import generics, filters
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
#from rest_framework.pagination import PageNumberPagination
from .paginations import ProductPagination


class ProductList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset= Product.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ("title", "brand__title")
    #filterset_fields = ("brand_id", "price")
    filterset_class = ProductFilter
    pagination_class = ProductPagination


class ProductRetrieve(generics.RetrieveAPIView):
    serializer_class =  ProductSerializer
    queryset = Product.objects.all()


class CreateProduct(generics.CreateAPIView):
     serializer_class = ProductSerializer


class ProductUpdate(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()    


class ProductRetrieveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryList(generics.ListAPIView):
    serializer_class =  CategorySerializer
    queryset = Category.objects.all()

 

class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()



        



