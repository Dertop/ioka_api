import json
import os
from pathlib import Path


class Config:
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / 'config.json'
        self.load_config()
    
    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.api_base_url = config.get('api', {}).get('base_url', 'http://localhost:5000')
                self.api_key = config.get('api', {}).get('api_key', 'test_api_key_12345')
                self.api_timeout = config.get('api', {}).get('timeout', 5)
                self.max_response_time_ms = config.get('test', {}).get('max_response_time_ms', 500)
                self.mock_server_port = config.get('test', {}).get('mock_server_port', 5000)
        else:
            self.api_base_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
            self.api_key = os.getenv('API_KEY', 'test_api_key_12345')
            self.api_timeout = int(os.getenv('API_TIMEOUT', '5'))
            self.max_response_time_ms = int(os.getenv('MAX_RESPONSE_TIME_MS', '500'))
            self.mock_server_port = int(os.getenv('MOCK_SERVER_PORT', '5000'))


config = Config()

