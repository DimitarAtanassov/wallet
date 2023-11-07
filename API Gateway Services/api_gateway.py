from flask import Flask, request, jsonify
import requests
import jwt
import hashlib
from web3 import Web3
import os
from pymongo import MongoClient

#Flask and Vars
app = Flask(__name__)
os.environ['GANACHE_URL'] = 'HTTP://127.0.0.1:7545'  # Replace with your desired URL
ganache_url = os.environ.get('GANACHE_URL')
account_priv_key = os.environ.get('ACCOUNT_PRIV_KEY')
public_key = os.environ.get('PUBLIC_KEY')



#For mongoDB 
"""client = MongoClient("")
db = client[""]
wallet_collection = db[""] """

"""Status Codes:
    1xx: Informational
    2xx: Success (Client request was successful)
    3xx: Redirection (Clieant must take additional actions in order for their request to be completed)
    4xx: Client Error (Error at client request)
    5xx: Server Error (Error at the server side)
    
""" 
#Generate JWT
#Encode JWT
#Use verify_jwt() to decode the token and see what the response looks like
#Start looking into ganache 

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
    
    # Get Transaction info from Front End and send transaction to Ganache
    data = request.json
    
    #Reterving Data from the json request
    to_address = data.get('to_address') # Address of the Reciever
    transaction_amount = data.get('transaction_amount') # Transaction Amount
    gas = data.get('gas')   # Represents cost of executing operations on the Ethereum Network
    gas_price = data.get('gas_price') #Amount of Ether a person is willing to pay for each unit of gas used in the transaction
    from_address = data.get('from_address') # Address of the Sender
    sender_private_key = data.get('private_key') # Private key of the Sender
    
    # Format data in order to send transaction to Ganache 
    amount_in_wei = w3.to_wei(transaction_amount,'ether') # Assuming the transaction amount will always be in ether when retrieved from Front End
    gas_price_in_wei = w3.to_wei(gas_price,'gwei') # Assuming gas_price will always be in gwei when retrieved from Front End
    
    # Valadating data
    if not (to_address and amount_in_wei and gas and gas_price_in_wei):
        return jsonify({"error": "Missing required parameters"}), 400
    
    # Connecting to Ganache
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    #Create transaction object that will be sent to Ganache
    transaction = {
        'to': to_address,
        'value': amount_in_wei,
        'gas': gas,
        'gasPrice': gas_price_in_wei,
        'nonce': w3.eth.getTransactionCount(from_address)
    }
    signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
 
    # Return the Transaction Hash after the transaction is complete
    return jsonify({"Transaction_Hash" : transaction_hash.hex()}), 200

