from django.shortcuts import render,redirect
from django.contrib import messages
from cart.cart import Cart



from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from store.models import Product,Profile
import datetime


def payment_success(request):
    return render(request,'payment/payment_success.html',{})

def checkout(request):
     #get the cart
    cart = Cart(request)

    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals= cart.cart_total()

    if request.user.is_authenticated:
        #checked out as a logged in user

        #get shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

         #get user shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        

   
        return render(request, "payment/checkout.html", {'cart_products': cart_products,"quantities":quantities,'totals':totals,"shipping_form":shipping_form})
    
    else:
        #checked out as a guest
        shipping_form = ShippingForm(request.POST or None)

        return render(request, "payment/checkout.html", {'cart_products': cart_products,"quantities":quantities,'totals':totals,"shipping_form":shipping_form})

def billing_info(request):
    if request.POST:
        #get the cart
        cart = Cart(request)

        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals= cart.cart_total()

        #create the session with shipping info

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping



       #check if user is logged in or not
        if request.user.is_authenticated:
            #for logged users
            #get billing Form
            billing_form = PaymentForm()

            return render(request, "payment/billing_info.html", {'cart_products': cart_products,"quantities":quantities,'totals':totals,"shipping_info":request.POST,'billing_form':billing_form})
        else:
            # for not logged users
            #get billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'cart_products': cart_products,"quantities":quantities,'totals':totals,"shipping_info":request.POST,'billing_form':billing_form})
    
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    

def process_order(request):
    if request.POST:

        #get the cart
        cart = Cart(request)

        cart_products = cart.get_prods
        
        quantities = cart.get_quants
        
        totals= cart.cart_total()

        # getting billing info form the last page
        payment_form = PaymentForm(request.POST or None)

        

        # get shipping session Data
        my_shipping = request.session.get('my_shipping')

        #gather the info
        full_name = my_shipping['shipping_full_name']

        email = my_shipping['shipping_email']
        
        
        #create shipping address from session info

        shipping_address =f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        
        amount_paid = totals

        #create an order

        if request.user.is_authenticated:
            #logged in
            user = request.user
            #create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #GET THE ORDER ID
            order_id = create_order.pk

            #get the product info
            for product in cart_products():
                #get product id
                product_id = product.id

                #get product price
                if product.is_onsale:
                    price = product.sale_price
                else:
                    price =product.price

                #get Quantity

                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, user=user, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

             # delete our cart
            for key in list(request.session.keys()):
                #delete the key
                if key == 'session_key':
                    del request.session[key]

            #delete the cart from datebase(old_cart field)

            current_user = Profile.objects.filter(user__id=request.user.id)

            #delete the cart from datebase(old_cart field)

            current_user.update(old_cart="")


            messages.success(request,'Order Placed')
            return redirect('home')
        else:
            #not logged in
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #GET THE ORDER ID
            order_id = create_order.pk

            #get the product info
            for product in cart_products():
                #get product id
                product_id = product.id

                #get product price
                if product.is_onsale:
                    price = product.sale_price
                else:
                    price =product.price

                #get Quantity

                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
            # delete our cart
            for key in list(request.session.keys()):
                #delete the key
                if key == 'session_key':
                    del request.session[key]

            messages.success(request,'Order Placed')
            return redirect('home')
        

    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:

        orders = Order.objects.filter(shipped=True)

        if request.POST:
            
            num = request.POST['num']

            #grab the order
            order = Order.objects.filter(id=num)

           #grab the date and time

            
            #update the order

            order.update(shipped=False)
            
            messages.success(request,"Shipping Status Updated")
            return redirect('shipped_dash')

        
        return render(request, "payment/shipped_dash.html", {'orders':orders})
    
    else:
        messages.success(request,'Access Denied')
        return redirect('home')

def not_shipped_dash(request):

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            
            num = request.POST['num']

            #grab the order
            order = Order.objects.filter(id=num)

           #grab the date and time

            now = datetime.datetime.now()
            #update the order

            order.update(shipped=True, date_shipped = now)
            
            messages.success(request,"Shipping Status Updated")
            return redirect('not_shipped_dash')

        return render(request, "payment/not_shipped_dash.html", {'orders':orders})
    
    else:
        messages.success(request,'Access Denied')
        return redirect('home')
    
def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        order = Order.objects.get(id=pk)

        #get the order items

        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']

            #check if true or false
            if status == "true":
                #get the order
                order = Order.objects.filter(id=pk)
                #update the status

                order.update(shipped=True)

                messages.success(request,"Shipping Status Updated")
                return redirect('not_shipped_dash')

            else:

                #get the order
                order = Order.objects.filter(id=pk)
                #update the status

                order.update(shipped=False)

                messages.success(request,"Shipping Status Updated")
                return redirect('shipped_dash')



        return render(request, "payment/orders.html", {'order':order,'items':items})
    
    else:
        messages.success(request,'Access Denied')
        return redirect('home')



    

    




    
