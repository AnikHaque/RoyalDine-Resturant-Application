from django.contrib import admin
from .models import AboutStory, AboutFeature, Chef, ContactMessage, UserProfile

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


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    # অ্যাডমিন লিস্টে যা যা কলাম থাকবে
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    
    # ডানপাশে ফিল্টার অপশন থাকবে (পড়া হয়েছে কি না বা তারিখ অনুযায়ী)
    list_filter = ('is_read', 'created_at')
    
    # নাম বা ইমেইল দিয়ে সার্চ করার অপশন
    search_fields = ('name', 'email', 'subject', 'message')
    
    # অ্যাডমিন লিস্ট থেকেই পড়া হয়েছে কি না তা টিক চিহ্ন দেওয়ার সুবিধা
    list_editable = ('is_read',)
    
    # মেসেজগুলো এমনভাবে আসবে যাতে নতুন মেসেজ সবার উপরে থাকে
    ordering = ('-created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'total_orders', 'membership_level')
    search_fields = ('user__username',)