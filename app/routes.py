from flask import Flask, render_template, abort, redirect, request
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

@app.route('/order/<product_id>', methods=['POST'])
def order(product_id):
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
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)

@app.route('/order/success')
def success():
    return render_template('success.html')


@app.route('/order/cancel')
def cancel():
    return render_template('cancel.html')