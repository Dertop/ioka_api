from typing import Tuple, Dict, Any
import requests
from utils.api_client import APIClient
from utils.validators import ResponseValidator


class TestHelpers:
    
    def __init__(self, api_client: APIClient, validator: ResponseValidator):
        self.api_client = api_client
        self.validator = validator
    
    def create_test_order(
        self,
        amount: float = 1000.0,
        currency: str = 'KZT',
        **kwargs
    ) -> Tuple[str, requests.Response]:
        response, _ = self.api_client.create_order(amount, currency, **kwargs)
        self.validator.assert_status_code(response, 201)
        order_id = response.json()['id']
        return order_id, response
    
    def create_test_payment(
        self,
        order_id: str,
        payment_method: str = 'card'
    ) -> Tuple[str, requests.Response]:
        response, _ = self.api_client.create_payment(order_id, payment_method)
        self.validator.assert_status_code(response, 201)
        payment_id = response.json()['id']
        return payment_id, response
    
    def create_order_and_payment(
        self,
        amount: float = 1000.0,
        currency: str = 'KZT',
        payment_method: str = 'card'
    ) -> Tuple[str, str, requests.Response, requests.Response]:
        order_id, order_response = self.create_test_order(amount, currency)
        payment_id, payment_response = self.create_test_payment(order_id, payment_method)
        return order_id, payment_id, order_response, payment_response

