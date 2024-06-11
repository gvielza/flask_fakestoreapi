from flask import Flask, render_template
import requests

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    url='https://fakestoreapi.com/products'
    response=requests.get(url)
    data=response.json()
    print(data)

    return render_template('productos.html',data=data)