from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Title")
    price = models.DecimalField(default=0, max_digits = 9, decimal_places = 2, null=False, blank=False)
    old_price = models.DecimalField(default=0, max_digits = 9, decimal_places = 2, null=False, blank=False)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    brand = models.ForeignKey("products.Brand", null=True, blank=True, on_delete = models.SET_NULL)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products" 


class Brand(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Title")

    class Meta:
        db_table = "brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands" 

    def __str__(self):
        return self.title    


class Category(models.Model):
    title = models.CharField(max_length=200, null=False, blank = False, verbose_name="Category")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, null=False, blank = False, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, null= False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "products_categories"
        verbose_name = "Product Category"
        verbose_name_plural = "Products Categories"

    def __str__(self):
       #return self.product.title
       return str(self.product) + " - " + self.category[0:5]+ ".."


class ProductReview(models.Model):
    review = models.TextField( null= True, blank=True)
    product = models.ForeignKey(Product, null=True, blank = True, on_delete=models.SET_NULL, related_name="reviews")

    class Meta:
        db_table = "products_reviews" 
        verbose_name = "Review" 
        verbose_name_plural = "Reviews"

    def __str__(self):
        #return self.product.title
         return str(self.product) + " - " + self.review[0:5]+ ".."

       




