from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
   
    return render(request, "cart_summary.html", {})


def cart_add(request):
   #get the cart
    cart = Cart(request)
    #test for POST

    if request.POST.get('action') == 'post':
        
        # Get product ID from request
        product_id = int(request.POST.get('product_id'))
            
        # Get product from database
        product = get_object_or_404(Product, id=product_id)

        # Add product to cart
        cart.add(product=product)

        # Return JSON response
        response = JsonResponse({'Product Name:': product.name })
        return response


def cart_delete(request):
    pass
    

def cart_update(request):
    pass
