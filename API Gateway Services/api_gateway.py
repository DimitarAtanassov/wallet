from flask import Flask, request, jsonify
import requests
import jwt
from web3 import Web3

app = Flask(__name)
ganache_url = "URL GOES HERE"
account_priv_key = "Private Account Key"


# Verify the authenticity and integrity of a JSON Web Token (JWT), which will be sent from wallet.js as a request
@app.route('/verify-jwt', methods=['POST'])
def verify_jwt():
    jwt_token = request.json['jwt']
    public_key = "some public key"
    try:
        data_payload = jwt.decode(jwt_token, public_key, algorithms=['RS256'])
        return jsonify(data_payload),200
    except jwt.exceptions.InvalidTokenError as err:
        print(repr(err))
        return 401
    except Exception as err:
        print(f"WARNING EXCEPTION CAUGHT: {repr(err)}")
        return 401
    # "JWT verification failed : 401 Error"

@app.route('/send-transaction', methods=['POST'])
def send_transaction(to_address, amount_in_wei, gas, gas_price):
    #Connect to Ganache Node
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    transaction = {
        'to': to_address,
        'value' : amount_in_wei,
        'gas' : gas,
        'gasPrice': w3.toWei(gas_price, 'gwei')
    }
