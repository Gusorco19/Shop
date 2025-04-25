from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'chameleons-key'

# Configuracion para Heroku PostgreSQL o SQLite local
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///shop.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))
    imagen = db.Column(db.String(200))

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar/<int:producto_id>')
def agregar(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    carrito = session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    session['carrito'] = carrito
    return redirect(url_for('index'))

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    items = []
    total = 0
    for id_str, cantidad in carrito.items():
        producto = Producto.query.get(int(id_str))
        items.append((producto, cantidad))
        total += producto.precio * cantidad
    return render_template('carrito.html', items=items, total=total)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
