from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Product, Category
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from .models import Command
from .forms import CommandForm
from django.contrib import messages

def home(request):
    featured_products = Product.objects.filter(featured=True).order_by('-date_added')[:8]
    context = {'featured_products': featured_products}
    return render(request, 'index.html', context=context)


def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'search_results.html', {'products': products, 'query': query, categories: categories})


def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}



def store(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()
    
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'products.html', {'products': products, 'categories': categories})


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
            return render(request, 'registration/register_done.html', {'new_user': new_user})
        else:
            # If the form is invalid, return the same form with error messages
            return render(request, 'registration/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})

    





def account_setting(request):
    return render(request, 'registration/account_settings.html')



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]  # Limit to 4 related products

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def command(request, product_id):
    if not request.user.is_authenticated:
        # Show the message
        messages.info(request, "Veuillez vous connecter pour commander ce produit.")
        print("hello######################")
        # Redirect to the login page, with a 'next' parameter to return back
        return redirect(f'{reverse("login")}?next={request.path}')

    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.user = request.user
            command.product = product
            command.save()
            # Optional: Send an email here
            return redirect('command_list')  # Redirect to user's command list after submitting
    else:
        form = CommandForm()

    return render(request, 'command_product.html', {'product': product, 'form': form})

@login_required
def command_list(request):
    commands = Command.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'command_list.html', {'commands': commands})
