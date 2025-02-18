from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    #get the cart
    cart = Cart(request)

    cart_products = cart.get_prods
    quantities = cart.get_quants

   
    return render(request, "cart_summary.html", {'cart_products': cart_products,"quantities":quantities})


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
        return response


def cart_delete(request):
    pass
    

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

        return response

