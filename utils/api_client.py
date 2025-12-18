import requests
import time
from typing import Dict, Any, Optional, Tuple
from utils.config import config


class APIClient:
    
    def __init__(self):
        self.base_url = config.api_base_url
        self.api_key = config.api_key
        self.timeout = config.api_timeout
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Tuple[requests.Response, float]:
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            request_headers = self.headers.copy()
            if data is None and method in ['POST', 'PUT', 'PATCH']:
                request_headers.pop('Content-Type', None)
            
            response = requests.request(
                method=method,
                url=url,
                json=data if data is not None else None,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )
            execution_time = (time.time() - start_time) * 1000
            return response, execution_time
        except requests.exceptions.RequestException as e:
            execution_time = (time.time() - start_time) * 1000
            raise Exception(f"Request failed: {str(e)}") from e
    
    def create_order(self, amount: float, currency: str = 'KZT', **kwargs) -> Tuple[requests.Response, float]:
        data = {
            'amount': amount,
            'currency': currency,
            **kwargs
        }
        return self._make_request('POST', '/orders', data=data)
    
    def get_order(self, order_id: str) -> Tuple[requests.Response, float]:
        return self._make_request('GET', f'/orders/{order_id}')
    
    def create_payment(self, order_id: str, payment_method: str = 'card') -> Tuple[requests.Response, float]:
        data = {'payment_method': payment_method}
        return self._make_request('POST', f'/orders/{order_id}/payments', data=data)
    
    def get_payment(self, payment_id: str) -> Tuple[requests.Response, float]:
        return self._make_request('GET', f'/payments/{payment_id}')
    
    def refund_payment(self, payment_id: str, amount: Optional[float] = None) -> Tuple[requests.Response, float]:
        data = {}
        if amount is not None:
            data['amount'] = amount
        return self._make_request('POST', f'/payments/{payment_id}/refund', data=data)

