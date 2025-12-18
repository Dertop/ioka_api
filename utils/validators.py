from typing import Dict, Any, List, Optional
import requests


class ResponseValidator:
    
    @staticmethod
    def assert_status_code(response: requests.Response, expected_code: int) -> None:
        assert response.status_code == expected_code, \
            f"Expected status code {expected_code}, got {response.status_code}"
    
    @staticmethod
    def assert_response_time(execution_time: float, max_time_ms: float) -> None:
        assert execution_time < max_time_ms, \
            f"Response time {execution_time:.2f}ms exceeds {max_time_ms}ms"
    
    @staticmethod
    def assert_json_structure(data: Dict[str, Any], required_fields: List[str]) -> None:
        for field in required_fields:
            assert field in data, f"Response should contain '{field}' field"
    
    @staticmethod
    def assert_error_structure(data: Dict[str, Any], expected_code: Optional[str] = None) -> None:
        assert 'error' in data, "Response should contain 'error' field"
        assert 'code' in data['error'], "Error should contain 'code' field"
        assert 'message' in data['error'], "Error should contain 'message' field"
        
        if expected_code:
            assert data['error']['code'] == expected_code, \
                f"Expected error code '{expected_code}', got '{data['error']['code']}'"
    
    @staticmethod
    def assert_field_value(data: Dict[str, Any], field: str, expected_value: Any) -> None:
        assert data.get(field) == expected_value, \
            f"Expected {field} to be {expected_value}, got {data.get(field)}"
    
    @staticmethod
    def assert_field_starts_with(data: Dict[str, Any], field: str, prefix: str) -> None:
        value = data.get(field, '')
        assert str(value).startswith(prefix), \
            f"Expected {field} to start with '{prefix}', got '{value}'"

