from flask import render_template, abort, redirect, request, session, url_for
import stripe
from app import app

products = {
    'bulk_granola': {
        'name': 'Bag of Granola 14 oz',
        'price': 1400,
    },
    'granola_bar': {
        'name': 'Granola Bar 3.5 oz',
        'price': 350,
        'per': 'bar',
        'adjustable_quantity': {
            'enabled': True,
            'minimum': 1,
            'maximum': 10,
        },
    },
}

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop', products=products)


# Latest update
@app.route('/order/<product_name>', methods=['POST'])
def order(product_name):
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    # =====================
    # Latest update
    # =====================

    # Get cart items
    cart_items = {}
    # Find items in cart
    try:
        if session:
            for product in session:
                cart_items[product] = session[product]
    except:
        cart_items = {}

    if product_name not in cart_items:
        abort(404)

    # =====================
    # End of latest update
    # =====================

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': cart_items[product_name]['name'],
                    },
                    'unit_amount': cart_items[product_name]['price'],
                    'currency': 'usd',
                },
                'quantity': 1,
                'adjustable_quantity': cart_items[product_name].get(
                    'adjustable_quantity',
                    {'enabled': False}
                ),
            },
        ],        

    shipping_address_collection={"allowed_countries": ["US", "CA"]},
    shipping_options=[
        {
        "shipping_rate_data": {
            "type": "fixed_amount",
            "fixed_amount": {"amount": 0, "currency": "usd"},
            "display_name": "Local Pickup"},
            },
        {
        "shipping_rate_data": {
            "type": "fixed_amount",
            "fixed_amount": {"amount": 700, "currency": "usd"},
            "display_name": "USPS Priority Mail",
            "delivery_estimate": {
            "minimum": {"unit": "business_day", "value": 4},
            "maximum": {"unit": "business_day", "value": 6},
                },
            },
        },
    ],

    payment_method_types=['card'],
    mode='payment',
    success_url=request.host_url + 'order/success',
    cancel_url=request.host_url + 'order/cancel',
    )
    del session[product_name]
    return redirect(checkout_session.url)



# Miguel's
@app.route('/miguel/order/<product_id>', methods=['POST'])
def product_order(product_id):
    stripe.api_key = app.config['STRIPE_SECRET_KEY']
    if product_id not in products:
        abort(404)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': products[product_id]['name'],
                    },
                    'unit_amount': products[product_id]['price'],
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],

    shipping_address_collection={"allowed_countries": ["US", "CA"]},
    shipping_options=[
    {
      "shipping_rate_data": {
        "type": "fixed_amount",
        "fixed_amount": {"amount": 0, "currency": "usd"},
        "display_name": "Local Pickup"},
        },
    {
      "shipping_rate_data": {
        "type": "fixed_amount",
        "fixed_amount": {"amount": 700, "currency": "usd"},
        "display_name": "USPS Priority Mail",
        "delivery_estimate": {
          "minimum": {"unit": "business_day", "value": 4},
          "maximum": {"unit": "business_day", "value": 6},
            },
        },
        },
    ],
        
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)




@app.route('/order/success')
def success():
    return render_template('success.html', title='Success')


@app.route('/order/cancel')
def cancel():
    return render_template('cancel.html', title='Cancel')


@app.route('/product/macbook')
def macbook():
    return render_template('products/macbook.html', title='Macbook')


@app.route('/add-to-cart/macbook')
def cart_macbook():
    session['macbook'] = {'name': 'Macbook Pro', 'price': 1799*100}
    return redirect(url_for('macbook'))


@app.route('/product/audio-technica')
def audio_technica():
    return render_template('products/audio_technica.html', title='Audio Technica')


@app.route('/add-to-cart/audio-technica')
def cart_audio_technica():
    session['audio-technica'] = {'name': 'Audio Technica', 'price': 169*100}
    return redirect(url_for('audio_technica'))


@app.route('/product/nothing-phone')
def nothing_phone():
    return render_template('products/nothing_phone.html', title='Nothing Phone')


@app.route('/add-to-cart/nothing-phone')
def cart_nothing_phone():
    session['nothing-phone'] = {'name': 'Nothing Phone', 'price': 499*100}
    return redirect(url_for('nothing_phone'))


@app.route('/cart')
def cart():
    cart_items = {}
    # Find items in cart
    try:
        if session:
            for product in session:
                cart_items[product] = session[product]
    except:
        cart_items = {}
    return render_template(
        'products/cart.html',
        title='Cart',
        cart_items=cart_items)


@app.route('/cart/delete/<product_name>')
def delete_cart_item(product_name):
    cart_items = {}
    # Find items in cart
    try:
        if session:
            for product in session:
                cart_items[product] = session[product]
    except:
        cart_items = {}

    for key in list(cart_items):
        print('cart items', key, cart_items[key])
        #if cart_items[key].name == product_name
        # if key.name == product_name:
        cart_items.pop(key)
        print(cart_items)
        del session[key]

    #cart_items.pop(product_name)
    # if session[product_name] in cart_items:
    #     del session[product_name]

    return redirect(url_for('cart'))
