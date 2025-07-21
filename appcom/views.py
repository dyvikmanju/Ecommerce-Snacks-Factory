from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse    
from .models import Product,Order,Address,Customer
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    category = request.GET.get('category', 'salty')  # default category
    products = Product.objects.filter(category=category)
    context = {
        'products': products,
        'active_category': category,
    }
    return render(request, "appcom/home.html", context)


@login_required
def ordering(request, id):
    product = get_object_or_404(Product, id=id)
    customer = Customer.objects.get(user=request.user)

    order, created = Order.objects.get_or_create(customer=customer, product=product,confirm=False)

    if created:
        order.quantity = 1
        messages.success(request, f"Added {product.name} to cart")
    else:
        order.quantity += 1
        messages.info(request, f"Increased quantity of {product.name} to {order.quantity}")

    order.save()

    return redirect("home")


 

@login_required
def cart(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    orders = customer.order_set.filter(confirm=False)
    total = 0
    for order in orders:
        total += order.product.price * order.quantity

    context = {
        'orders': orders,
        'total': total
    }
    return render(request, 'appcom/cart.html', context)




@login_required
def address(request):
    customer = Customer.objects.get(user=request.user)
    orders = customer.order_set.filter(confirm=False)

    if request.method == "POST":
        if "add_address" in request.POST:
            # Adding a new address
            addr = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip_code')

            Address.objects.create(
                customer=customer,
                address=addr,
                city=city,
                state=state,
                zip_code=zip_code
            )
            messages.success(request, "Address added successfully.")
            return redirect('address')

        elif "confirm_address" in request.POST:
            # Confirming to a selected address

            address_id = request.POST.get('confirm_address')
            address = Address.objects.get(id=address_id, customer=customer)
            orders.update( address=address)

            # ✅ Total amount for payment (convert to cents)
            total_amount = sum(order.quantity * order.product.price for order in orders)
            stripe_amount = int(total_amount * 100)  # e.g., 1234 => ₹12.34

            # ✅ Create Stripe checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': stripe_amount,
                        'product_data': {
                            'name': f"{request.user.username}'s Order",
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment-success/'),  # Use absolute URL
                cancel_url=request.build_absolute_uri('/payment-cancel/'),
            )
            return redirect(session.url, code=303)
            # messages.success(request, "Order confirmed to selected address.")
            # return redirect('payment')  # or a summary page
    all_addresses = Address.objects.filter(customer=customer)  # same as  ads = customer.address_set.all()
    return render(request, 'appcom/address.html', {'addresses': all_addresses,'customer':customer})


def product_detail(request,id):
    product1 = get_object_or_404(Product, id=id)
    context={'product':product1}
    return render(request,'appcom/product_detail.html',context)


def update_quantity(request, id):
    order = get_object_or_404(Order, id=id, customer__user=request.user)  # order = get_object_or_404(Order, id=id)
# will work, but it's less secure, especially in multi-user systems.
#  What's the Issue?
# If you don't check that the order belongs to the logged-in user, then any logged-in user could modify another user's cart just by changing the id in the URL.
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "inc":
            order.quantity += 1
            order.save()
            messages.success(request, f"Increased quantity of {order.product.name}")
        elif action == "dec":
            if order.quantity > 1:
                order.quantity -= 1
                order.save()
                messages.info(request, f"Decreased quantity of {order.product.name}")
            else:
                order.delete()
                messages.warning(request, f"Removed {order.product.name} from cart")

    return redirect("cart") 





@login_required
def confirmed_orders(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(confirm=True, customer=customer)
    context = {'orders': orders}
    return render(request, 'appcom/confirmed_orders.html', context)

def about(r):
    return render(r,'appcom/about.html')



@login_required
def payment_success(request):
    customer = Customer.objects.get(user=request.user)
    customer.order_set.filter(confirm=False).update(confirm=True)

    return render(request, 'appcom/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'appcom/payment_cancel.html')












def learning_view(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    addresses = Address.objects.all()
    orders = Order.objects.all()

    context = {
        'customers': customers,
        'products': products,
        'addresses': addresses,
        'orders': orders
    }
    return render(request, 'appcom/learning.html', context)








from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_orders(request):
    delivered_orders = Order.objects.filter(confirm=True, delivered=True)
    pending_orders = Order.objects.filter(confirm=True, delivered=False)
    context = {
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'appcom/admin_orders.html', context)

@staff_member_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delivered = True
    order.save()
    messages.success(request, f"Order #{order.id} marked as delivered.")
    return redirect('admin_orders')






from .forms import ProductForm

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')  # or redirect to product list
    else:
        form = ProductForm()
    return render(request, 'appcom/add_product.html', {'form': form})


def new_arraival(request):
    
    return render(request, 'appcom/new_arraival.html')