from flask import Flask, render_template, jsonify, request
import requests
from productos_api import productos as prod

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

@app.route('/carrito/<int:id>', methods=['POST'])
def carrito(id):
    title=request.form.get('title')
    image=request.form.get('image')
    price=request.form.get('price')
    cantidad=request.form.get('count')
    print(title)
    print(image)
    print(price)
    print(cantidad)
    return render_template('carrito.html', id=id, title=title, image=image,price=price, cantidad=cantidad)


@app.route('/carrito/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    return render_template('carrito.html', id=id)

@app.route("/api/productos/", methods=["GET"])
def api():
    return jsonify(prod)