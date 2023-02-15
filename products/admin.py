from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'old_price', 'brand', 'quantity']
    search_fields = ['title',]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title',]
    search_fields = ['title',]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'id']
    search_fields = ['title', ]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'category', ]
    search_fields = ['review']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['review', 'product']
    search_fields = ['review']




    

