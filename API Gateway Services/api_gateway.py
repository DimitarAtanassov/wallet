from flask import Flask, request, jsonify
from web3 import Web3
import os
import config
from flask_cors import CORS

# Flask and Vars
app = Flask(__name__)
CORS(app)
ganache_url = "HTTP://127.0.0.1:7545"



# Generate JWT
# Encode JWT
# Use verify_jwt() to decode the token and see what the response looks like
# Start looking into ganache 

# For mongoDB 
"""
client = MongoClient("")
db = client[""]
wallet_collection = db[""]
"""

"""
Status Codes:
1xx: Informational
2xx: Success (Client request was successful)
3xx: Redirection (Client must take additional actions to complete their request)
4xx: Client Error (Error at client request)
5xx: Server Error (Error at the server side)
"""

# Uncomment the following lines if needed
# @app.route('/verify-jwt', methods=['POST'])
# def verify_jwt():
#     data = request.json
#     jwt_token = data.get('jwt')
#     if not jwt_token:
#         return jsonify({"error": "Missing JWT token"}), 400
#
#     try:
#         data_payload = jwt.decode(jwt_token, public_key, algorithms=['RS256'])
#         return jsonify(data_payload), 200
#     except jwt.exceptions.InvalidTokenError as err:
#         print(repr(err))
#         return jsonify({"error": "Invalid token"}), 401
#     except Exception as err:
#         print(f"WARNING EXCEPTION CAUGHT: {repr(err)}")
#         return jsonify({"error": "Server error"}), 500

@app.route('/send-transaction', methods=['POST'])
def send_transaction():
    # Get Transaction info from Front End and send transaction to Ganache
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid or empty JSON in the request body"}), 400
    
    to_address = "0x0d6079727FcD9eBbd5D4a74846fbD5Bd2b02055B"
    # Retrieving Data from the json request
    transaction_amount = data.get('transaction_amount')  # Transaction Amount
    gas = data.get('gas')  # Represents cost of executing operations on the Ethereum Network
    gas_price = data.get('gas_price')  # Amount of Ether a person is willing to pay for each unit of gas used in the transaction
    from_address = data.get('from_address')  # Address of the Sender
    sender_private_key = data.get('sender_private_key')  # Private key of the Sender
    # Connecting to Ganache
    try:
        w3 = Web3(Web3.HTTPProvider(ganache_url))
        print("Connection to Blockchain Successful")
    except requests.exceptions.RequestException:
        return jsonify({"error": "Connection to Ganache failed"}), 500
    # Format data to send transaction to Ganache
    amount_in_wei = w3.to_wei(transaction_amount, 'ether')
    gas_price_in_wei = w3.to_wei(gas_price, 'gwei')
    
    

    # Validating data
    if (
            not all([transaction_amount, gas, gas_price, from_address, sender_private_key]) or
            not isinstance(transaction_amount, (int, float)) or
            not isinstance(gas, int) or
            not isinstance(gas_price, int) or
            not isinstance(from_address, str) or
            not isinstance(sender_private_key, str)
    ):
        return jsonify({"error": "Parameters are missing or invalid"}), 400

    
    try:
        # Create transaction object that will be sent to Ganache
        transaction = {
            'to': to_address,
            'from' : from_address,
            'value': amount_in_wei,
            'gas': gas,
            'gasPrice': gas_price_in_wei,
            'nonce': w3.eth.get_transaction_count(from_address)
        }
        signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)
        transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        # Return the Transaction Hash after the transaction is complete
        return jsonify({"Transaction_Hash": transaction_hash.hex(),
                        "Transaction_Status" : True
                        }), 200
    except ValueError as e:
        err_msg = str(e)
        if "insufficient funds for gas * price + value" in err_msg:
            return jsonify({"error": "Insufficient funds for transaction",
                            "Transaction_Status" : False}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)