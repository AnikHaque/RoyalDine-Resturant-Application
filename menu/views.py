from django.shortcuts import render, get_object_or_404
from .models import Category

def menu_view(request):
    categories = Category.objects.prefetch_related('foods')
    return render(request, 'menu.html', {'categories': categories})


def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    foods = category.foods.filter(is_available=True)

    context = {
        "category": category,
        "foods": foods
    }
    return render(request, "category_items.html", context)
