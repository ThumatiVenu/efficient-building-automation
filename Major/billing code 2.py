import uuid
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog

class Cafeteria:
    def __init__(self):
        self.orders = []

    def place_order(self, items):
        order_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        order = {
            'order_id': order_id,
            'items': items,
            'timestamp': timestamp,
            'status': 'unpaid'
        }
        self.orders.append(order)
        return order_id

    def get_order(self, order_id):
        for order in self.orders:
            if order['order_id'] == order_id:
                return order
        return None

    def update_order_status(self, order_id, status):
        for order in self.orders:
            if order['order_id'] == order_id:
                order['status'] = status
                return True
        return False

class PaymentGateway:
    def __init__(self):
        self.transactions = []

    def make_payment(self, order_id, amount):
        transaction_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        transaction = {
            'transaction_id': transaction_id,
            'order_id': order_id,
            'amount': amount,
            'timestamp': timestamp,
            'status': 'success'
        }
        self.transactions.append(transaction)
        return transaction_id

    def get_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction['transaction_id'] == transaction_id:
                return transaction
        return None

class BillingSystem:
    def __init__(self):
        self.cafeteria = Cafeteria()
        self.payment_gateway = PaymentGateway()

    def place_order(self, items):
        order_id = self.cafeteria.place_order(items)
        return order_id

    def get_order(self, order_id):
        return self.cafeteria.get_order(order_id)

    def update_order_status(self, order_id, status):
        return self.cafeteria.update_order_status(order_id, status)

    def make_payment(self, order_id, amount):
        transaction_id = self.payment_gateway.make_payment(order_id, amount)
        if transaction_id:
            self.update_order_status(order_id, 'paid')
        return transaction_id

    def get_transaction(self, transaction_id):
        return self.payment_gateway.get_transaction(transaction_id)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Dynamic input for order details using Tkinter
    item_name = simpledialog.askstring("Input", "Enter the billing name:")
    quantity = simpledialog.askinteger("Input", "Enter quantity:")
    price = simpledialog.askfloat("Input", "Enter price of bill:")

    # Calculate the total amount
    total_amount = quantity * price

    # Create an instance of the BillingSystem class
    billing_system = BillingSystem()

    # Place an order with dynamically entered details
    order_id = billing_system.place_order([{'name': item_name, 'quantity': quantity, 'price': price}])
    print(f"Order ID: {order_id}")

    # Get and display the order details
    order = billing_system.get_order(order_id)
    print(f"Order: {order}")

    # Make a payment with the calculated amount
    transaction_id = billing_system.make_payment(order_id, total_amount)
    print(f"Transaction ID: {transaction_id}")

    # Get and display the transaction details
    transaction = billing_system.get_transaction(transaction_id)
    print(f"Transaction: {transaction}")

if __name__ == "__main__":
    main()