from flask import Flask, request
from ib_insync import *

app = Flask(__name__)

# Connect to IBKR TWS (paper trading) via a secure tunnel like ngrok or localhost
ib = IB()
ib.connect('host.docker.internal', 7497, clientId=1)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)

    contract = Stock('MU', 'SMART', 'USD')
    action = data.get('action', '').upper()

    if action in ['BUY', 'SELL']:
        order = MarketOrder(action, 10)
        ib.placeOrder(contract, order)
        return f"{action} order placed", 200

    return "Invalid action", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
