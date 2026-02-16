from django.db import models
from django.contrib.auth.models import User
from menu.models import Food
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum

# --- পাইথন কাস্টম ম্যানেজার (গিটহাব পার্সেন্টেজ ও লজিক বাড়াবে) ---
class OrderManager(models.Manager):
    def total_revenue(self):
        """শুধুমাত্র পেইড অর্ডার থেকে মোট আয় বের করার লজিক"""
        return self.filter(is_paid=True).aggregate(Sum('total_price'))['total_price__sum'] or Decimal('0.00')

class Order(models.Model):
    """
    অর্ডার ম্যানেজমেন্ট মডেল। পেমেন্ট এবং ডেলিভারি স্ট্যাটাস আলাদা রাখা হয়েছে।
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PREPARING', 'Preparing'),
        ('ON_THE_WAY', 'On The Way'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=100, default="Guest Customer")
    phone = models.CharField(max_length=20, default="0000000000")
    address = models.TextField(default="No Address Provided")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # --- নতুন পেমেন্ট ফিল্ড (এটিই আপনার প্রবলেম সলভ করবে) ---
    is_paid = models.BooleanField(default=False) 
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    delivery_man = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_deliveries'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ম্যানেজার অ্যাসাইন করা
    objects = OrderManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Order"

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.status})"

    # --- পাইথন লজিক সেকশন ---

    @property
    def is_delivered(self):
        return self.status == 'DELIVERED'

    @property
    def delivery_duration(self):
        if self.created_at:
            diff = timezone.now() - self.created_at
            return int(diff.total_seconds() / 60)
        return 0

    def calculate_tax(self, tax_rate=Decimal('0.05')):
        return (self.total_price * tax_rate).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.strip().title()
        self.phone = self.phone.replace(" ", "")
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True)
    combo_id = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food.name if self.food else 'Combo Item'}"

    @property
    def subtotal(self):
    # যদি প্রাইস বা কোয়ান্টিটি কোনো কারণে None হয়, তবে যেন ০ রিটার্ন করে
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity