from django.db import models
from django.contrib.auth.models import User  # Import User model

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)  

    def __str__(self):
        return self.user.username

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('sweet', 'Sweet'),
        ('spicy', 'Spicy'),
        ('salty', 'Salty'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='imagesss/', blank=True)

    # New field
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='sweet',
        help_text="Select the taste category"
    )
    def __str__(self):
        return self.name
    
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()  
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)  

    def __str__(self):
        return f"{self.customer.user.username}'s Address is {self.city}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1) 
    confirm=models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    delivered = models.BooleanField(default=False)


    def __str__(self):
        return f"Order #{self.id} - {self.customer} ordered {self.quantity} {self.product}"
    
    @property
    def pro_price(self):
        return self.quantity * self.product.price


    

