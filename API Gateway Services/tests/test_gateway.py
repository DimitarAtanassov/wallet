import unittest
import json
from api_gateway import app

class apiGateWayTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    # 400 -> Bad Request (Cause of Bad Request is missing params)
    def test_send_transaction_missing_parameters(self):
        response = self.app.post('/send-transaction', json={})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual({}, {"error" : "Parameters are missing or invalid"})
    
    # Mimics a successful transaction
    def test_send_transaction_success(self):
        data = {
            'to_address': '0xRecipientAddress',
            'transaction_amount': 1,  # 1 Ether
            'gas': 21000,  # A typical gas amount for simple transfers
            'gas_price': 1000000000,  # 1 Gwei
            'from_address': '0xSenderAddress',
            'private_key': 'valid_private_key',
        }
        response = self.app.post('/send-transaction', json=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Transaction_Hash", data)
    
    # Testing to see if insufficient funds for transaction will be denied
    def test_send_transaction_insufficient_funds(self):
        
        data = {
            'to_address': '0xRecipientAddress',
            'transaction_amount': 100000000000000000000000000,  # 1 Ether
            'gas': 21000,  # A typical gas amount for simple transfers
            'gas_price': 1000000000,  # 1 Gwei
            'from_address': '0xSenderAddress',
            'private_key': 'valid_private_key',
        }
        response = self.app.post("/send-transaction", json=data)
        self.assertEqual(response.status_code,400)
        data = json.loads(response.data.decde('utf-8'))
        self.assertEqual(data,{"error" : "Insufficient funds for transaction"})
    
    # Testing to see if ganache connection failure will be processed
    def test_send_transaction_ganache_connection_failure(self):
        with unittest.mock.patch('config.GANACHE_URL', 'http://nonexistenturl:8545'):
               response = self.app.get('/send-transaction')  # Find out actual endpoint that connects to ganache and replace '/send-transaction' with the endpoint
               self.assertEqual(response.status_code, 500)