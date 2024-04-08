from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Customer(models.Model):
    user=  models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    address=models.CharField(max_length=50)
    email=models.EmailField(unique=True, max_length=255)
    mobile_no=models.CharField(max_length=10,unique=True)
    joined_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('user', 'email', 'mobile_no')

class Product(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, blank=True, null=True)
    make = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    price=models.PositiveIntegerField()
    key_features = models.TextField()
    technical_specifications = models.TextField()
    technical_catalogue = models.URLField(blank=True)
    user_manual = models.URLField(blank=True)
    datasheet = models.URLField(blank=True)
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/')
    image3 = models.ImageField(upload_to='product_images/')
    image4 = models.ImageField(upload_to='product_images/')
    image5 = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)  # Assuming product_name is the field you want to use
        super().save(*args, **kwargs)
 
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_submission_timestamp = models.DateTimeField(null=True, blank=True)

    def calculate_total(self):
        return sum(cart_product.subtotal for cart_product in self.cartproduct_set.all())
    
def __str__(self):
  return f"Cart: {self.id}, Customer: {self.customer}, Total: {self.total}, Created at: {self.created_at}"


class Cartproduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE) 
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True) 
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Calculate subtotal based on quantity and product price
        self.subtotal = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
      return f"Cart: {self.cart.id}, Cartproduct: {self.id}, Product: {self.product}, Quantity: {self.quantity}, Subtotal: {self.subtotal}"
    

class Solution(models.Model):
    name=models.CharField(max_length=50)
    category=models.CharField(max_length=20)

    def _str_(self):
        return self.name            

class Newsletter(models.Model):
    email=models.EmailField(unique=True)
  
    def _str_(self):
        return self.email           
