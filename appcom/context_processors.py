# appcom/context_processors.py

from .models import Order
from django.db.models import Sum

def cart_quantity(request):
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = (
            Order.objects.filter(customer__user=request.user,confirm=False)
            .aggregate(Sum('quantity'))['quantity__sum'] or 0
        )
    return {'total_quantity': total_quantity}


# simple code



# def cart_quantity(request):
# total_quantity = 0
# if request.user.is_authenticated:
#     orders = Order.objects.filter(customer__user=request.user)
#     for order in orders:
#         total_quantity += order.quantity
# return {'total_quantity': total_quantity}
