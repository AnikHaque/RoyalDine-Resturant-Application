from django.db import models
from django.db import models
from cloudinary.models import CloudinaryField

class AboutStory(models.Model):
    title = models.CharField(max_length=200, default="Authentic Flavors, Traditional Recipes.")
    description = models.TextField()
    experience_years = models.IntegerField(default=15)
    main_image = CloudinaryField('main_image', folder='about/')
    
    class Meta:
        verbose_name_plural = "About Story"

class AboutFeature(models.Model):
    icon_class = models.CharField(max_length=100, help_text="FontAwesome class (e.g., fa-leaf)")
    title = models.CharField(max_length=100)
    description = models.TextField()

class Chef(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='chefs/')
    order = models.IntegerField(default=0) # কার ছবি আগে দেখাবে তার জন্য

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
