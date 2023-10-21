from flask import Flask, request, jsonify
import requests
import jwt
from web3 import Web3
import os

app = Flask(__name__)
ganache_url = os.environ.get('GANACHE_URL')
account_priv_key = os.environ.get('ACCOUNT_PRIV_KEY')
public_key = os.environ.get('PUBLIC_KEY')

@app.route('/verify-jwt', methods=['POST'])
def verify_jwt():
    data = request.json
    jwt_token = data.get('jwt')
    if not jwt_token:
        return jsonify({"error": "Missing JWT token"}), 400

    try:
        data_payload = jwt.decode(jwt_token, public_key, algorithms=['RS256'])
        return jsonify(data_payload), 200
    except jwt.exceptions.InvalidTokenError as err:
        print(repr(err))
        return jsonify({"error": "Invalid token"}), 401
    except Exception as err:
        print(f"WARNING EXCEPTION CAUGHT: {repr(err)}")
        return jsonify({"error": "Server error"}), 500

@app.route('/send-transaction', methods=['POST'])
def send_transaction():
    data = request.json
    to_address = data.get('to_address')
    amount_in_wei = data.get('amount_in_wei')
    gas = data.get('gas')
    gas_price = data.get('gas_price')

    if not (to_address and amount_in_wei and gas and gas_price):
        return jsonify({"error": "Missing required parameters"}), 400

    w3 = Web3(Web3.HTTPProvider(ganache_url))
    # account_address = os.environ.get('ACCOUNT_ADDRESS')

    transaction = {
        'to': to_address,
        'value': amount_in_wei,
        'gas': gas,
        'gasPrice': w3.toWei(gas_price, 'gwei'),
        # 'nonce': w3.eth.getTransactionCount(account_address)
    }

    ##------------ transaction logic -------------
    # signed_txn = w3.eth.account.signTransaction(transaction, account_priv_key)
    # txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # return jsonify({"transaction_hash": txn_hash.hex()}), 200

