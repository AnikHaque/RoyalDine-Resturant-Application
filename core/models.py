from django.db import models

class HeroSection(models.Model):
    sub_title = models.CharField(max_length=100, default="Est. 2012 • Fine Dining")
    main_title_white = models.CharField(max_length=100, default="Crafting")
    main_title_span = models.CharField(max_length=50, default="Moments")
    main_title_bottom = models.CharField(max_length=100, default="Beyond Taste")
    menu_button_text = models.CharField(max_length=50, default="View Our Menu")
    story_button_text = models.CharField(max_length=50, default="Our Story")
    background_image = models.ImageField(upload_to='banner/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "1. Hero Section"

class RestaurantFeature(models.Model):
    icon_class = models.CharField(max_length=50, help_text="e.g., fas fa-leaf")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "2. Restaurant Features"