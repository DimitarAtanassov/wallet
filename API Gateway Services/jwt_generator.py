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
amount_eth = 10 
amount_wei = w3.to_wei(amount_eth,'ether')
gas = 50000
gas_price_gwei = 20
gas_price_wei = w3.to_wei(gas_price_gwei,'gwei')
to_address = "0xdf36eFD9a38C7A687B7b660f4537d800806BCb55"
from_address = "0x14dBc93d7098F2284fd410e344736f50F19C7EAe"

#Payload: Data
transaction = {
    'to': to_address,
    'value': amount_wei,
    'gas': gas,
    'gasPrice': gas_price_wei,
    'nonce': w3.eth.get_transaction_count(from_address)
}


#Private key of sender used to sign the transaction
private_key = "0x0778f3fcc88d794d1992d96ea6f870cd2ea330aa8c79c9ab12fb762cebe50152"

# Sign and send the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

#Transaction hash info
print(f"Transaction Hash: {transaction_hash.hex()}")