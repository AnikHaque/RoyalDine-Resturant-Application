from django.db import models
from django.contrib.auth.models import User
from menu.models import Food, ComboDeal # কম্বো মডেল ইমপোর্ট করলাম

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    # এখানে null=True, blank=True দিলাম যাতে কম্বো হলে খাবার খালি রাখা যায়
    food = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # কম্বোর জন্য নতুন রাস্তা বানালাম
    combo = models.ForeignKey(
        ComboDeal, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Item for Order #{self.order.id}"