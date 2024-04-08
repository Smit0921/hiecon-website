from .models import Cart, Customer

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        user_carts = Cart.objects.filter(customer=customer)
        if user_carts.exists():
            user_cart = user_carts.first()
            cart_count = user_cart.cartproduct_set.count()

    return {'cart_count': cart_count}
