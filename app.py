from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "transaction.json"

def load_transactions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_transactions(transactions):
    with open(DATA_FILE, "w") as file:
        json.dump(transactions, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_transaction():
    symbol = request.form['symbol']
    result = request.form['result']
    notes = request.form['notes']
    date = request.form['date']

    transactions = load_transactions()
    transactions.append({
        'symbol': symbol,
        'result': result,
        'notes': notes,
        'date': date
    })
    save_transactions(transactions)

    return redirect(url_for('transactions'))

@app.route('/position_calculator', methods=['GET', 'POST'])
def position_calculator():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        stop_loss_percentage = float(request.form['stop_loss_percentage'])

        leverage = amount / (stop_loss_percentage * 0.01)

        return render_template('position_calculator.html', position_size=leverage)

    return render_template('position_calculator.html')

@app.route('/transactions')
def transactions():
    transactions = load_transactions()
    return render_template('transactions.html', transactions=transactions)

@app.route('/tradepnl', methods=['GET', 'POST'])
def tradepnl():
    if request.method == 'POST':
        symbol = request.form['symbol']
        result = request.form['result']
        notes = request.form['notes']
        date = request.form['date']

        transactions = load_transactions()
        transactions.append({
            'symbol': symbol,
            'result': result,
            'notes': notes,
            'date': date
        })
        save_transactions(transactions)

        return redirect(url_for('transactions'))
    else:
        return render_template('tradepnl.html')

@app.route('/mydata', methods=['GET', 'POST'])
def mydata():
    if request.method == 'POST':
        balance = request.form['balance']
        save_amount(balance)
        return redirect(url_for('mydata'))
    else:
        balance = load_amount()
        return render_template('mydata.html', balance=balance)

def load_amount():
    if not os.path.exists("data.txt"):
        return ""
    with open("data.txt", "r") as file:
        return file.read()

def save_amount(balance):
    with open("data.txt", "w") as file:
        file.write(balance)

if __name__ == '__main__':
    app.run(debug=True)
