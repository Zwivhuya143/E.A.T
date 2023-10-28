from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    parent_id = models.IntegerField(null=True, default=None)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    new_field =models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "category"

class Product(models.Model):
    #referencing the categories 
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, default=None)   
    product_id = models.AutoField(primary_key = True, editable = False, unique=True)
    name = models.CharField(max_length=255)    
    description = models.TextField(blank=True)    
    price = models.DecimalField(max_digits=10, decimal_places=2)   
    image = models.ImageField(null=True, blank=True, upload_to='images/' )

    def __str__(self):        
        return self.name
    
    class Meta:
        db_table = "product"

class SKU(models.Model):    
    sku_id = models.AutoField(primary_key=True, unique=True)    
    sku = models.CharField(max_length=255, unique=True)   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)   
    quantity_in_stock = models.IntegerField()    
    color = models.CharField(max_length=255)   
    size = models.CharField(max_length=255)

    def __str__(self):        
        return f"{self.sku} {self.color} {self.size}"
    
    class Meta:
        db_table = "sku"


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    cart_status = models.CharField(max_length=255, null=True, blank=True)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):       
         return f"{self.user} {self.cart_id}"
    
    class Meta:
        db_table = "cart"


class Order(models.Model):    
    order_id = models.AutoField(primary_key=True)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    address = models.TextField()    
    order_status = models.CharField(max_length=255)    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):       
        return f"{self.user} {self.order_id}"
    
    class Meta:
        db_table = "order"


class OrderItem(models.Model):    
    order_item_id = models.AutoField(primary_key=True)    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    quantity = models.IntegerField()

    def __str__(self):       
        return f"{self.order_item_id} {self.order} {self.product}"
    
    class Meta:
        db_table = "order_item"



class CartItem(models.Model):    
    cart_item_id = models.AutoField(primary_key=True)    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    quantity = models.IntegerField(default=0)

    def __str__(self):        
        return f"{self.cart_item_id} {self.cart} {self.product}"
    
    class Meta:
        unique_together = ("cart", "product")
        db_table = "cart_item"
        