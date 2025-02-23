from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    #get the cart
    cart = Cart(request)

    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals= cart.cart_total()

   
    return render(request, "cart_summary.html", {'cart_products': cart_products,"quantities":quantities,'totals':totals})


def cart_add(request):
   #get the cart
    cart = Cart(request)
    #test for POST

    if request.POST.get('action') == 'post':
        
        # Get product ID from request
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
            
        # Get product from database
        product = get_object_or_404(Product, id=product_id)

        # Add product to cart
        cart.add(product=product, quantity=product_qty)

        #get cart Quantity

        cart_quantity = cart.__len__()

        # Return JSON response
        # response = JsonResponse({'Product Name:': product.name })

        
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Item Added To Your Shopping Cart  ..!"))
        return response


def cart_delete(request):
    #get the cart
    cart = Cart(request)
    #test for POST

    if request.POST.get('action') == 'post':
        
        # Get product ID from request
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, ("Item Deleted From Your Shopping Cart  ..!"))

        return response
    
    
    

def cart_update(request):
    #get the cart
    cart = Cart(request)
    #test for POST

    if request.POST.get('action') == 'post':
        
        # Get product ID from request
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Your Shopping Cart Has Been Updated  ..!"))

        return response

