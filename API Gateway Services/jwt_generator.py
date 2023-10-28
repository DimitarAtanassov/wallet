#Generate a JWT token
import jwt
from web3 import Web3


#Connecting to web3 with Ganache 
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:5000"))

#Header: Algo & Token Type
#   Alg: Signature / Encryption Algo
#   Typ: Type of token
jwt_header = {
    "alg":"RS256",
    "typ": "JWT"
}

# Values to be used in Payload(Transaction)
amount_eth = 10 
amount_wei = w3.to_wei(amount_eth,'ether')
gas = 50000
gas_price_gwei = 20
gas_price_wei = w3.to_wei(gas_price_gwei,'gwei')
to_address = "0xae01BcD0bBAa2Bd3B1abE0b910ABe14A0Ea8f85d"
from_address = "0x7Ee06E3a8FCdFB11D41f8F2872b7327A7fC5fcE5"

#Payload: Data
transaction = {
    'to': to_address,
    'value': amount_wei,
    'gas': gas,
    'gasPrice': gas_price_wei,
    'nonce': w3.eth.get_transaction_count(from_address)
}


#Private key of sender used to sign the transaction
private_key = "0xc86fc1439e1deb777e4fc60e54a9192412c3ba3fc2a7f6c86ba2a0aa1115bab1"

# Sign and send the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

#Transaction hash info
print(f"Transaction Hash: {transaction_hash.hex()}")