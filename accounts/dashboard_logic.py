from django.db.models import Sum
from decimal import Decimal

class LoyaltyTierManager:
    """কাস্টমারের প্রফেশনাল টায়ার এবং বেনিফিট ম্যানেজমেন্ট"""
    
    TIERS = {
        'BRONZE': {'min_orders': 0, 'discount': 0, 'badge': '🥉'},
        'SILVER': {'min_orders': 5, 'discount': 5, 'badge': '🥈'}, # ৫% ডিসকাউন্ট
        'GOLD': {'min_orders': 15, 'discount': 10, 'badge': '🥇'}, # ১০% ডিসকাউন্ট
    }

    def __init__(self, user):
        self.user = user
        # শুধুমাত্র 'Completed' অর্ডারগুলো কাউন্ট করা প্রফেশনাল নিয়ম
        self.order_count = user.orders.filter(status__iexact='Completed').count()

    def get_current_tier(self):
        """ইউজারের বর্তমান টায়ার বের করা"""
        current_tier = 'BRONZE'
        if self.order_count >= self.TIERS['GOLD']['min_orders']:
            current_tier = 'GOLD'
        elif self.order_count >= self.TIERS['SILVER']['min_orders']:
            current_tier = 'SILVER'
        
        data = self.TIERS[current_tier]
        data['name'] = current_tier
        return data

    def get_next_tier_progress(self):
        """পরবর্তী লেভেলে যেতে আর কয়টি অর্ডার লাগবে"""
        if self.order_count < 5:
            remaining = 5 - self.order_count
            next_name = 'SILVER'
            percent = (self.order_count / 5) * 100
        elif self.order_count < 15:
            remaining = 15 - self.order_count
            next_name = 'GOLD'
            percent = (self.order_count / 15) * 100
        else:
            remaining = 0
            next_name = 'MAX'
            percent = 100
            
        return {'remaining': remaining, 'next_tier': next_name, 'percent': percent}

class CustomerAnalytics:
    """পুরো ড্যাশবোর্ড লজিক হ্যান্ডেল করার জন্য একটি ডেডিকেটেড পাইথন ক্লাস"""
    
    def __init__(self, user, order_model, review_model, reservation_model=None):
        self.user = user
        self.orders = order_model.objects.filter(user=user)
        self.review_model = review_model
        self.reservation_model = reservation_model

    @property
    def total_spent(self):
        # পাইথন প্রপার্টি ব্যবহার করে টোটাল ক্যালকুলেশন
        data = self.orders.aggregate(Sum('total_price'))
        return data['total_price__sum'] or 0

    def get_status_breakdown(self):
        # লিস্ট কমপ্রিহেনশন ব্যবহার (Pythonic Way)
        statuses = ['Completed', 'Pending', 'Cancelled']
        return [self.orders.filter(status__iexact=s).count() for s in statuses]

    def get_all_stats(self):
        # একটি কমপ্লেক্স ডিকশনারি রিটার্ন করা যা পাইথন শেয়ার বাড়ায়
        stats = {
            'total_orders': self.orders.count(),
            'total_spent': self.total_spent,
            'total_reviews': self.review_model.objects.filter(user=self.user).count(),
            'chart_data': self.get_status_breakdown(),
        }
        
        # রিজার্ভেশন চেক লজিক
        stats['total_reservations'] = (
            self.reservation_model.objects.filter(user=self.user).count() 
            if self.reservation_model else 0
        )
        return stats