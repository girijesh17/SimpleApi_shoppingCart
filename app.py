from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session handling

# Static list of available items
available_items = {
    # Electronics
    "Laptop": 45000,
    "Smartphone": 25000,
    "Tablet": 20000,
    "Smartwatch": 5500,

    # Accessories
    "Mouse": 500,
    "Keyboard": 800,
    "Headphones": 1500,
    "Webcam": 2000,
    "Charger": 700,
    "Pen Drive": 600,
    "Hard Disk": 3200,
    "Power Bank": 1200,
    "Speakers": 2200,
    "Bluetooth Earbuds": 1800,

    # Networking
    "Router": 1800,
    "LAN Cable": 300,
    "WiFi Adapter": 950,

    # Home Appliances
    "Washing Machine": 32000,
    "Microwave Oven": 11000,
    "LED TV": 38000,
    "Ceiling Fan": 2600,

    # Stationery
    "Notebook": 80,
    "Pen Pack": 50,
    "Calculator": 300,
    "Geometry Box": 120,
    "Stapler": 100,

    # Groceries
    "Rice 5kg": 280,
    "Wheat Flour 5kg": 230,
    "Sugar 1kg": 50,
    "Tea Powder 250g": 120,
    "Cooking Oil 1L": 160
}


cart = []

@app.route('/', methods=['GET', 'POST'])
def index():
    total = sum(item['price'] * item['quantity'] for item in cart)
    if request.method == 'POST':
        session['customer_id'] = request.form['customer_id']
        session['customer_name'] = request.form['customer_name']
        session['customer_phone'] = request.form['customer_phone']
    return render_template('index.html', cart=cart, total=total, items=available_items, session=session)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['item']
    quantity = int(request.form['quantity'])
    price = available_items[name]

    for item in cart:
        if item['name'] == name:
            item['quantity'] += quantity
            return redirect(url_for('index'))

    item_id = len(cart) + 1
    cart.append({'id': item_id, 'name': name, 'price': price, 'quantity': quantity})
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    new_quantity = int(request.form['quantity'])
    for item in cart:
        if item['id'] == item_id:
            item['quantity'] = new_quantity
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    global cart
    cart = [item for item in cart if item['id'] != item_id]
    return redirect(url_for('index'))

@app.route('/bill')
def print_bill():
    total = sum(item['price'] * item['quantity'] for item in cart)
    date_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    return render_template(
        'bill.html',
        cart=cart,
        total=total,
        customer_id=session.get('customer_id', ''),
        customer_name=session.get('customer_name', ''),
        customer_phone=session.get('customer_phone', ''),
        date_time=date_time
    )

if __name__ == '__main__':
    app.run(debug=True)
