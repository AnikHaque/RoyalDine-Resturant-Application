from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy (Celebration)'),
        ('stressed', 'Stressed (Comfort Food)'),
        ('romantic', 'Romantic (Date Night)'),
        ('lazy', 'Lazy (Quick Bites)'),
    ]
    mood_tag = models.CharField(max_length=20, choices=MOOD_CHOICES, default='happy')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image', folder='foods/')
    is_available = models.BooleanField(default=True)
    is_today_special = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    calories = models.IntegerField(default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    carbs = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    ai_tags = models.CharField(max_length=255, blank=True, null=True)
    is_surprise_item = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Offer(models.Model):
    food = models.ForeignKey(
        'Food',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0)

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.food:
            return f"{self.title} - {self.food.name}"
        return self.title

    @property
    def discounted_price(self):
        if not self.food:
            return 0

        if not self.discount_percentage:
            return self.food.price

        discount = (self.food.price * self.discount_percentage) / 100
        return self.food.price - discount

    @property
    def is_valid(self):
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.IntegerField()
    image = CloudinaryField('image', folder='testimonials/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s review"
    

class ComboDeal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', folder='combos/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class FlashDeal(models.Model):
    title = models.CharField(max_length=200, default='The "Gemini" Mega Combo')
    description = models.TextField()
    discount_text = models.CharField(max_length=50, default='40% OFF')
    image = CloudinaryField('image', folder='deals/')
    end_time = models.DateTimeField() 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def time_remaining(self):
        return self.end_time > timezone.now()