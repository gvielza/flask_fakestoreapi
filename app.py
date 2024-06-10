from flask import Flask, render_template,url_for

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')