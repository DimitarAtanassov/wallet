#Generate a JWT token
import jwt
from web3 import Web3,Account


#Connecting to web3 with Ganache 
to_address = "0xae01BcD0bBAa2Bd3B1abE0b910ABe14A0Ea8f85d" # Davids Wallet

from_address = "0x0d6079727FcD9eBbd5D4a74846fbD5Bd2b02055B" # User wallet address
private_key = "0x8c58cb12c008afc88bf76d224977b1dbdee2d96f70cd908e1510eb0cf9b528a3"
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
amount_eth = 10 
amount_wei = w3.to_wei(amount_eth,'ether')
gas = 6721975
gas_price_gwei = 20
gas_price_wei = w3.to_wei(gas_price_gwei,'gwei')




# Get accounts
accounts_in_ganache = w3.eth._accounts()

# Create new account for the user sending money with their private key 
user_balance_before = w3.eth.get_balance(from_address)
ganache_balance_before = w3.eth.get_balance(to_address)


#Balances before transaction
print(f"Ganache Bal B4: {ganache_balance_before}")
print(f"New Account Bal B4: {user_balance_before}")
transaction = {
    'to' : to_address,
    'from' : from_address,
    'value' : w3.to_wei(5,'ether'),
    'gas' : 6721975,
    'gasPrice': gas_price_wei,
    'nonce': w3.eth.get_transaction_count(from_address)
}
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print(f"Hash: {transaction_hash}")
ganache_bal_after = w3.eth.get_balance(to_address)
print(f"Ganache Bal After: {ganache_bal_after}")
# Values to be used in Payload(Transaction)



#Payload: Data
# transaction = {
#     'to': to_address,
#     'value': amount_wei,
#     'gas': gas,
#     'gasPrice': gas_price_wei,
#     'nonce': w3.eth.get_transaction_count(from_address)
# }


#Private key of sender used to sign the transaction
#private_key = "0xc86fc1439e1deb777e4fc60e54a9192412c3ba3fc2a7f6c86ba2a0aa1115bab1"

# Sign and send the transaction
# signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
# print(signed_transaction.rawTransaction)
# transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

#Transaction hash info
print(f"Transaction Hash: {transaction_hash.hex()}")


    


