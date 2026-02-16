from django.contrib import admin
from .models import AboutStory, AboutFeature, Chef

# ১. স্টোরি ম্যানেজমেন্ট (যাতে অ্যাডমিন প্যানেলে সুন্দর দেখায়)
@admin.register(AboutStory)
class AboutStoryAdmin(admin.ModelAdmin):
    # যেহেতু স্টোরি একটাই হবে, তাই লিস্টে বেশি কিছু দরকার নেই
    list_display = ('title', 'experience_years')

# ২. ফিচার ম্যানেজমেন্ট
@admin.register(AboutFeature)
class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class')

# ৩. শেফ ম্যানেজমেন্ট
@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'order')
    list_editable = ('order',) # অ্যাডমিন লিস্ট থেকেই সিরিয়াল চেঞ্জ করা যাবে

