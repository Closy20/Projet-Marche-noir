from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    imageUser = models.ImageField(upload_to='appli1/PHOTO', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    preferences = models.CharField(max_length=15,blank=True, null=True)
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='appli1/PHOTO', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='non-vendu')

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'

class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_made')
    reviewee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_received')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.reviewer} for {self.reviewee}'

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment of {self.amount} by {self.user}'

class Transaction(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sales')
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction of {self.product} from {self.seller} to {self.buyer}'