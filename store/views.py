from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required




def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context=context)

def register(request):
    pass
  
    


@login_required(login_url='login')
def order_product(request, product_id):
    # Check if the user is a superuser
    if request.user.is_superuser:
        return redirect('home')  # Redirect superusers to home or any other page
    
    # Logic for regular users to order the product
    return render(request, 'order.html', {})


def account_setting(request):
    return render(request, 'registration/account_settings.html')