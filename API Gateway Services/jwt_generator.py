#Generate a JWT token
import jwt
from web3 import Web3


#Connecting to web3 with Ganache 
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

#Header: Algo & Token Type
#   Alg: Signature / Encryption Algo
#   Typ: Type of token
jwt_header = {
    "alg":"RS256",
    "typ": "JWT"
}

# Values to be used in Payload(Transaction)
amount_eth = 200 
amount_wei = w3.to_wei(amount_eth,'ether')
gas = 6721975
gas_price_gwei = 20
gas_price_wei = w3.to_wei(gas_price_gwei,'gwei')
to_address = "0x0a39E65631Df544256EE3f06833De5915181af5F"
from_address = "0xed30e1dF671Fa865a73d94fA251529CD8d7BFC23"

#Payload: Data
transaction = {
    'to': to_address,
    'value': amount_wei,
    'gas': gas,
    'gasPrice': gas_price_wei,
    'nonce': w3.eth.get_transaction_count(from_address)
}


#Private key of sender used to sign the transaction
private_key = "0x01a8f5ad7784d9d4f191ee9a469a80695ae26b70c4e533c713df70244d9407d0"

# Sign and send the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

#Transaction hash info
print(f"Transaction Hash: {transaction_hash.hex()}")