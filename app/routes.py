from flask import Flask, render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop')
