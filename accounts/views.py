
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from appcom.models import Customer
from .models import Register
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # saves the User
            mobile = form.cleaned_data.get('phone')  # get the mobile number
            email = form.cleaned_data.get('email')

            # Save to Customer model (optional if using signals)
            Customer.objects.update_or_create(user=user, defaults={'phone': mobile})

            Register.objects.create(user=user, phone=mobile,email=email)

            login(request, user)  # log user in after signup
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})