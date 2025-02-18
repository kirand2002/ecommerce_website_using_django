class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session cart if it exists, otherwise create a new empty cart
        cart = self.session.get('session_key')

        # If cart doesn't exist in session, initialize it
        if 'session_key' not in request.session:
            cart= self.session['session_key'] = {}

    # make sure cart id=s available on all pages of site
        self.cart = cart
    
    def add(self, product):
        product_id = str(product.id)


        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price' : str(product.price)}

        self.session.modified = True

    