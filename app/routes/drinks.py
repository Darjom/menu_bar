from flask import Blueprint, render_template, request, redirect, url_for
import json
import os

drinks_bp = Blueprint('drinks', __name__)

# Rutas de los archivos de datos
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../data'))
DRINKS_FILE = os.path.join(DATA_PATH, 'drinks.json')
ORDERS_FILE = os.path.join(DATA_PATH, 'orders.json')


# Cargar la lista de tragos
def load_drinks():
    with open(DRINKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# Cargar los pedidos existentes
def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# Guardar los pedidos
def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


# Página principal con la lista de tragos
@drinks_bp.route('/', methods=['GET'])
def home():
    drinks = load_drinks()
    return render_template('home.html', drinks=drinks)


# Guardar un pedido
@drinks_bp.route('/pedido', methods=['POST'])
def place_order():
    print("⚠️ DEBUG: Ingresando a /pedido")
    print("🔢 request.method:", request.method)
    print("📦 request.form:", request.form)

    selected = request.form.getlist('selected_drinks')
    print("📋 selected_drinks:", selected)

    if selected:
        orders = load_orders()
        orders.append(selected)
        save_orders(orders)
        print("✅ Pedido guardado:", orders)
    else:
        print("❌ Nada seleccionado...")

    return redirect(url_for('drinks.home', pedido='ok'))



# Vista para bartenders con los pedidos actuales
@drinks_bp.route('/bartender', methods=['GET'])
def bartender_view():
    pedidos = load_orders()
    return render_template('bartender.html', pedidos=pedidos)


# Marcar un pedido como servido
@drinks_bp.route('/marcar-servido', methods=['POST'])
def serve_order():
    index = int(request.form['order_index'])
    orders = load_orders()
    if 0 <= index < len(orders):
        del orders[index]
        save_orders(orders)
    return redirect(url_for('drinks.bartender_view'))
