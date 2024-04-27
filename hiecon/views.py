from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomerRegistrationForm,LoginForm,NewsletterSubscriptionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import ListView,DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from smtplib import SMTPException
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from .forms import ProductSearchForm
# from django.contrib.auth.models import User


# Create your views here.
def Index(request):
    cart_count = 0
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        user_carts = Cart.objects.filter(customer=customer)
        if user_carts.exists():
            user_cart = user_carts.first()
            cart_count = user_cart.cartproduct_set.count()

    return render(request, 'index.html', {'cart_count': cart_count})

def About(request):
    return render(request,'about.html')

def Service(request):
    return render(request,'services.html')

def Contact(request):
    return render(request,'contact.html')

def Team(request):
    return render(request,'team.html')

def handle_query_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Send email
        send_mail(
            subject,
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            email,  # Sender's email
            ['smit.hiecon18@gmail.com'],  # Your email to receive the query
            fail_silently=False,
        )

        # You can customize the response as per your requirement
        return JsonResponse({'message': 'Form submitted successfully!'})

    # Return an empty response if the request method is not POST
    return JsonResponse({}, status=405)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 8  # Set to 8 products per page

    def get_queryset(self):
        # Start with all products
        queryset = Product.objects.all()
        
        # Check if there is a search query
        search_query = self.request.GET.get('query')
        if search_query:
            # Filter products based on the search query
            queryset = queryset.filter(product_name__icontains=search_query)
        
        # Additional filtering based on category, subcategory, and make (brand)
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        make = self.request.GET.get('make')

        if category:
            queryset = queryset.filter(category=category)
        if subcategory:
            queryset = queryset.filter(subcategory=subcategory)
        if make:
            queryset = queryset.filter(make=make)
        
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Additional context data (e.g., categories, brands) can be added here
        # Fetch distinct categories
        categories = Product.objects.values_list('category', flat=True).distinct()
        context['categories'] = categories

        # Fetch distinct makes (brands)
        makes = Product.objects.values_list('make', flat=True).distinct()
        
        # Create a dictionary to hold makes and their product counts
        make_product_counts = {}
        for make in makes:
            count = Product.objects.filter(make=make).count()  # Count products for each make
            make_product_counts[make] = count
        
        # Add makes and their counts to context
        context['makes_with_counts'] = make_product_counts
        
        # Organize categories with subcategories and products
        categories_with_products = {}
        for category in categories:
            subcategories = Product.objects.filter(category=category).values_list('subcategory', flat=True).distinct()
            subcategories_with_products = {}
            
            for subcategory in subcategories:
                # Filter products based on category and subcategory
                products = Product.objects.filter(category=category, subcategory=subcategory)
                # Store the product names for each subcategory
                subcategories_with_products[subcategory] = [product.product_name for product in products]
            
            # Store subcategories with products for each category
            categories_with_products[category] = subcategories_with_products
        
        # Add categories with products to context
        context['categories_with_products'] = categories_with_products
        
        # Add selected make to context for the template
        context['selected_make'] = self.request.GET.get('make')
        
        layout = self.request.GET.get('layout', 'grid')  # Default layout to grid

        # Add the layout choice to context
        context['selected_layout'] = layout
        context['search_query'] = self.request.GET.get('query', '')

        # Check if any products were found
        context['products_found'] = context['products'].exists()

        # Fetch distinct categories and makes
        context['categories'] = Product.objects.values_list('category', flat=True).distinct()
        context['makes'] = Product.objects.values_list('make', flat=True).distinct()

        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        lookup = self.kwargs.get(self.slug_url_kwarg)
        if lookup.isdigit():
            # If it's a digit, treat it as an ID
            return get_object_or_404(Product, pk=lookup)
        else:
            # Otherwise, treat it as a slug
            return get_object_or_404(Product, slug=lookup)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the product object
        product = context['product']

        # Create a list of image URLs from the product object
        images = []
        for image_num in range(1, 6):
            image_field = getattr(product, f'image{image_num}', None)
            if image_field and image_field.url:
                images.append(image_field.url)
      
        
        # Get the current product's category and subcategory
        current_category = self.object.category
        current_subcategory = self.object.subcategory

        # Retrieve similar products from the same category and subcategory
        similar_products = Product.objects.filter(category=current_category, subcategory=current_subcategory).exclude(pk=self.object.pk)  
        # [:3]

        # Add the similar products to the context
        context['similar_products'] = similar_products
        context['images'] = images
        return context

def create_user(request):
    if request.method == 'POST':
        userform = CustomerRegistrationForm(request.POST)
        if userform.is_valid():
            try:
                user = userform.save()
                customer = Customer.objects.create(
                    user=user,
                    name=userform.cleaned_data['name'],
                    address=userform.cleaned_data['address'],
                    email=userform.cleaned_data['email'],
                    mobile_no=userform.cleaned_data['mobile_no']
                )
                messages.success(request, 'Account created successfully.')
                return redirect('login')
            except IntegrityError:
                # Log the error for debugging purposes, but don't expose details to the user
                #  messages.error(request, 'An error occurred during registration. Please try again.')
                pass
        else:
            # The form is invalid, but client-side validation will handle this
            pass
    else:
        userform = CustomerRegistrationForm()

    return render(request, 'register.html', {'userform': userform})

def Login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                # Log the user in
                login(request, user)
                return redirect('index')  # Redirect to the appropriate page after login
            else:
                # Inactive user account
                messages.error(request, 'Your account is disabled.')
        else:
            # Invalid login credentials
            messages.error(request, 'Invalid username or password')

    # If the request is not POST or authentication fails, render the login page again
    return render(request, 'login.html')
    
def Logout_view(request):
    if request.user.is_authenticated:
     logout(request)
    return redirect('index')

def view_cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        
        # Get all carts associated with the customer
        user_carts = Cart.objects.filter(customer=customer)
        
        # Choose the desired behavior, e.g., display contents of the first cart
        if user_carts.exists():
            user_cart = user_carts.first()
            cart_products = user_cart.cartproduct_set.all()
            total_cost = user_cart.calculate_total()
            return render(request, 'cart.html', {'cart_products': cart_products, 'total_cost': total_cost})
        else:
            return HttpResponse("Your cart is empty.")
    else:
         messages.error(request,"Please log in to view your cart.")
         return redirect('login')
       

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user)

        # Get all carts associated with the customer
        user_carts = Cart.objects.filter(customer=customer)

        # Choose the desired behavior, e.g., add the product to the first cart found
        if user_carts.exists():
            user_cart = user_carts.first()
        else:
            # If no carts found, create a new one
            user_cart = Cart.objects.create(customer=customer)

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('product-list')  # Redirect to your product list page or any other page

        # Check if the product is already in the cart
        cart_product, created = Cartproduct.objects.get_or_create(
            cart=user_cart,
            product=product,
            defaults={'quantity': 1, 'subtotal': product.price}
        )

        # If the product is already in the cart, update the quantity and subtotal
        if not created:
            cart_product.quantity += 1
            cart_product.subtotal = cart_product.quantity * cart_product.product.price
            cart_product.save()

        messages.success(request, f"{product.product_name} added to your cart successfully.")
        return redirect('product-list')  # Redirect to your product list page or any other page
    else:
        messages.warning(request, "Please log in to add products to your cart.")
        return redirect('login')  # Redirect to your login page or any other page

def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(Cartproduct, id=cart_product_id)
    cart_product.delete()
    messages.success(request, 'Product removed from the cart.')

    return redirect('cart')

def update_quantity(request, cart_product_id):
    cart_product = get_object_or_404(Cartproduct, id=cart_product_id)
    action = request.GET.get('action')

    if action == 'increment':
        cart_product.quantity += 1
    elif action == 'decrement':
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
        else:
            messages.error(request, 'Minimum 1 quantity needed.')
            messages.get_messages(request).used = True

    cart_product.subtotal = cart_product.quantity * cart_product.product.price
    cart_product.save()
    messages.success(request, 'Quantity updated successfully.')
    return redirect('cart')

      
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user)

        # Get all carts associated with the customer
        user_carts = Cart.objects.filter(customer=customer)

        # Choose the desired behavior, e.g., add the product to the first cart found
        if user_carts.exists():
            user_cart = user_carts.first()
        else:
            # If no carts found, create a new one
            user_cart = Cart.objects.create(customer=customer)

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('product-list')  # Redirect to your product list page or any other page

        # Check if the product is already in the cart
        cart_product, created = Cartproduct.objects.get_or_create(
            cart=user_cart,
            product=product,
            defaults={'quantity': 1, 'subtotal': product.price}
        )

        # If the product is already in the cart, update the quantity and subtotal
        if not created:
            cart_product.quantity += 1
            cart_product.subtotal = cart_product.quantity * cart_product.product.price
            cart_product.save()

        messages.success(request, f"{product.product_name} added to your cart successfully.")
        return redirect('product-list')  # Redirect to your product list page or any other page
    else:
        messages.warning(request, "Please log in to add products to your cart.")
        return redirect('login')  # Redirect to your login page or any other page

def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(Cartproduct, id=cart_product_id)
    cart_product.delete()
    messages.success(request, 'Product removed from the cart.')

    return redirect('cart')

def update_quantity(request, cart_product_id):
    cart_product = get_object_or_404(Cartproduct, id=cart_product_id)
    action = request.GET.get('action')

    if action == 'increment':
        cart_product.quantity += 1
    elif action == 'decrement':
        if cart_product.quantity > 1:
            cart_product.quantity -= 1
        else:
            messages.error(request, 'Minimum 1 quantity needed.')
            messages.get_messages(request).used = True

    cart_product.subtotal = cart_product.quantity * cart_product.product.price
    cart_product.save()
    messages.success(request, 'Quantity updated successfully.')
    return redirect('cart')


def submit_cart(request):
    if request.method == 'POST':
        user = request.user
        customer, created = Customer.objects.get_or_create(user=user)

        # Ensure that there's only one cart associated with the customer
        user_cart = Cart.objects.filter(customer=customer).first()
        if not user_cart:
            user_cart = Cart.objects.create(customer=customer)

        cart_products = user_cart.cartproduct_set.all()

        # Construct email message
        admin_email = "smit.hiecon18@gmail.com"  # Replace with your admin's email
        subject = f"New Cart Submission - {user.username}"
        message = f"{user.username} submitted the following items:\n"
        for cart_product in cart_products:
            message += f"{cart_product.product.product_name} - Quantity: {cart_product.quantity}\n"

        # Update last_submission_timestamp
        user_cart.last_submission_timestamp = timezone.now()
        user_cart.save()

        # Create a new cart for the user
        new_user_cart = Cart.objects.create(customer=customer)

        # Set cart foreign key to new_user_cart for all associated Cartproduct instances
        cart_products.update(cart=new_user_cart)
        messages.success(request, 'Thank you. Your Cart is Submitted.')

        # Send email to admin
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
            print("Email sent successfully!")
        except Exception as e:
            print(f"Email sending failed: {e}")

    return redirect('cart')

def check_availability(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')

        if field == 'Username':
            exists = User.objects.filter(username=value).exists()
        elif field == 'Email':
            exists = User.objects.filter(email=value).exists()
        elif field == 'Mobile number':
            exists = User.objects.filter(customer__mobile_no=value).exists()
        else:
            exists = False

        return JsonResponse({'field': field, 'available': not exists})
    else:
        return JsonResponse({'available': False}) 
    
class SolutionDetailView(TemplateView):
    template_name = 'solution_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        solutions = Solution.objects.filter(category=category)
        context['category'] = category
        context['solutions'] = solutions
        return context


def newsletter_subscribe(request):
    # message = None

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                # User is already subscribed
                message = 'You are already subscribed.'
            else:
                form.save()
                message = 'Thank you for subscribing!'
        else:
            if 'email' in form.errors:
                message = 'You are already subscribed.'
    
    return render(request, 'index.html', {'message': message})