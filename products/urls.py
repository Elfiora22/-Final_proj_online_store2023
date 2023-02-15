from django.urls import path
from .views import *


urlpatterns = [
  
#Product paths
    path('all/', ProductList.as_view(), name="list_of_products"),
    path('get/<int:pk>/', ProductRetrieve.as_view(), name="product_find"),
    path('product-create/', CreateProduct.as_view(), name="product_create_post"),
    path('get/<int:pk>/delete/', ProductRetrieveDestroy.as_view(), name="category_find_delete"),
    path('<int:pk>/update/', ProductUpdate.as_view(), name="update_prod_patch_put"),

]