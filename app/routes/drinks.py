from flask import Blueprint, render_template, request, redirect, url_for
import json
import os

drinks_bp = Blueprint('drinks', __name__)

# Cargar los tragos desde el archivo JSON
def load_drinks():
    data_path = os.path.join(os.path.dirname(__file__), '../../data/drinks.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@drinks_bp.route('/', methods=['GET'])
def home():
    drinks = load_drinks()
    return render_template('home.html', drinks=drinks)

@drinks_bp.route('/pedido', methods=['POST'])
def place_order():
    selected = request.form.getlist('selected_drinks')
    print("Pedido recibido:", selected)  # Aquí puedes almacenar en archivo, db o Firebase
    return redirect(url_for('drinks.home'))
