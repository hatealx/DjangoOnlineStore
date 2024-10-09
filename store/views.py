from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from alimentation import settings
from .models import Product, Category
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from .models import Command
from .forms import CommandForm
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import BadHeaderError

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
        messages.info(request, "Veuillez vous connecter pour commander ce produit.")
        return redirect(f'{reverse("login")}?next={request.path}')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.user = request.user
            command.product = product
            command.save()

            # Prepare the email content for the store owner
            subject = f"Nouvelle commande pour {product.name}"
            message = f"""
                Prénom: {form.cleaned_data['first_name']}
                Nom: {form.cleaned_data['last_name']}
                Email: {request.user.email}  # Use email from the authenticated user
                Numéro de téléphone: {form.cleaned_data['phone_number']}
                
                Détails de la commande:
                {form.cleaned_data['command_details']}  # Include the entire content entered by the user

                Produit commandé: {product.name}
                Prix: {product.price} FCFA
            """

            # Prepare the confirmation email content for the user
            user_email_subject = f"Confirmation de commande pour {product.name}"
            user_email_message = f"""
                Bonjour {request.user.first_name} {request.user.last_name},

                Merci d'avoir commandé chez nous !

                Votre commande pour {product.name} a bien été reçue.
                Voici les détails de votre commande :
                
                {form.cleaned_data['command_details']}  # Include the whole content in the user's email

                Prix: {product.price} FCFA

                Nous vous contacterons bientôt pour la livraison.

                Cordialement,
                L'équipe de la boutique ElizAb
            """

            try:
                # Send emails to store owner and user
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['aatsou12@gmail.com'],
                    fail_silently=False,
                )

                send_mail(
                    user_email_subject,
                    user_email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )

                # Redirect to confirmation page after the command
                return redirect('command_done')  # Redirect to the 'command done' page

            except (BadHeaderError, TimeoutError) as e:
                # Show error message and allow the user to retry
                messages.error(request, "Une erreur s'est produite lors de l'envoi de votre commande. Veuillez réessayer.")
                # Optionally, log the error for debugging
                print(f"Email sending failed: {e}")

                # Allow the user to retry submitting the form
                return render(request, 'command_product.html', {'product': product, 'form': form})

    else:
        form = CommandForm()

    return render(request, 'command_product.html', {'product': product, 'form': form})


@login_required
def command_done(request):
    return render(request, 'command_done.html')


@login_required
def command_list(request):
    commands = Command.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'command_list.html', {'commands': commands})
