import base64
from datetime import timedelta

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests
from productos_api import productos as prod
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from marshmallow import Schema, fields, validate, ValidationError


load_dotenv()

app=Flask(__name__)
app.secret_key=os.environ.get('SECRET_KEY')

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default-secret-key')

CLIENT_ID=os.environ.get('CLIENT_ID')
CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'https://gvielza.pythonanywhere.com/callback'
SCOPES = 'user-top-read'

api_key_clash_royale =os.environ.get('api_key_clash_royale')

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

@app.route("/spotify")
def spotify():
    return render_template('spotify.html')

@app.route('/login')
def login():
    auth_url = (
        'https://accounts.spotify.com/authorize'
        '?response_type=code'
        f'&client_id={CLIENT_ID}'
        f'&scope={SCOPES}'
        f'&redirect_uri={REDIRECT_URI}'
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    session['access_token'] = response_data['access_token']
    return redirect(url_for('top_artists'))

@app.route('/top_artists')
def top_artists():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    top_artists = response.json()
    artists_list = """
    <html>
    <head>
        <style>
            ol {
                list-style-type: none;
                padding: 0;
            }
            li {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            img {
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Mis artistas más escuchados</h1>
        <ol>
    """
    for idx, artist in enumerate(top_artists['items'][:10], start=1):
        artist_name = artist['name']
        artist_image_url = artist['images'][0]['url'] if artist['images'] else ''
        artists_list += f"<li>{idx}. <img src='{artist_image_url}' alt='{artist_name}' style='height:50px;'> {artist_name}</li>"
    artists_list += "</ol></body></html>"
    return artists_list

@app.route("/clash_royale")
def clash_royale():
    return render_template('clash_royale.html')

@app.route('/cartas')
def obtener_cartas():
    url = 'https://api.clashroyale.com/v1/cards'
    headers = {
        'Authorization': f'Bearer {api_key_clash_royale}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un código de error
        data = response.json()
        return render_template('cartas.html', cartas=data['items'])
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Error al obtener las cartas: {e}')
        return jsonify({'error': 'No se pudieron obtener las cartas'}), 500


@app.route('/obtener_ip')
def obtener_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return jsonify(ip_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mi_api', methods=['GET'])
@jwt_required()
def mi_api():
    data={
        'message':'Hola esta en mi API de productos',
        'status':"success"
    }
    return jsonify(data)

jwt = JWTManager(app)
with app.app_context():
    # Crear un token de acceso manualmente dentro del contexto de la aplicación
    token = create_access_token(identity="user", expires_delta=timedelta(hours=1))
    print(f"Token JWT: {token}")
@app.route('/mi_api', methods=['POST'])
@jwt_required()
def mi_api_post():
    if(request.is_json == True):
        data = request.get_json()
        response = {
            'message': 'Datos Recibidos',
            'status': 'success',
            'data': data
        }
        print(data)
        return jsonify(response), 200
    else:
        data = {
            'message': 'No se recibieron datos',
            'status': 'error'
        }
    return jsonify(data)






