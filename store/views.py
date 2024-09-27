from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm


def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context=context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            return render(request,'registration/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(
        request,
        'registration/register.html',
        {'user_form': user_form}
        )
    


@login_required(login_url='login')
def order_product(request, product_id):
    # Check if the user is a superuser
    if request.user.is_superuser:
        return redirect('home')  # Redirect superusers to home or any other page
    
    # Logic for regular users to order the product
    return render(request, 'order.html', {})


def account_setting(request):
    return render(request, 'registration/account_settings.html')


