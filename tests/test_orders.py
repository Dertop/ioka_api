import allure
from utils.config import config
from utils.validators import ResponseValidator


@allure.feature("Orders API")
@allure.story("Create Order")
class TestCreateOrder:
    
    def test_create_order_success(self, api_client, validator, mock_server):
        with allure.step("Create order with valid data"):
            response, execution_time = api_client.create_order(
                amount=1000.0,
                currency='KZT',
                description='Test order'
            )
        
        with allure.step("Verify status code is 201"):
            validator.assert_status_code(response, 201)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify response structure"):
            data = response.json()
            validator.assert_json_structure(data, ['id', 'amount', 'currency', 'status', 'created_at'])
        
        with allure.step("Verify response values"):
            validator.assert_field_value(data, 'amount', 1000.0)
            validator.assert_field_value(data, 'currency', 'KZT')
            validator.assert_field_value(data, 'status', 'pending')
            validator.assert_field_starts_with(data, 'id', 'order_')
    
    def test_create_order_missing_amount(self, api_client, validator, mock_server):
        with allure.step("Create order without amount"):
            response, execution_time = api_client._make_request('POST', '/orders', data={'currency': 'KZT'})
        
        with allure.step("Verify status code is 400"):
            validator.assert_status_code(response, 400)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'VALIDATION_ERROR')
    
    def test_create_order_invalid_amount(self, api_client, validator, mock_server):
        with allure.step("Create order with zero amount"):
            response, execution_time = api_client.create_order(amount=0, currency='KZT')
        
        with allure.step("Verify status code is 400"):
            validator.assert_status_code(response, 400)
        
        with allure.step("Verify error message"):
            validator.assert_error_structure(response.json(), 'VALIDATION_ERROR')
    
    def test_create_order_empty_body(self, api_client, validator, mock_server):
        with allure.step("Create order with empty body"):
            response, execution_time = api_client._make_request('POST', '/orders', data=None)
        
        with allure.step("Verify status code is 400"):
            validator.assert_status_code(response, 400)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify error structure"):
            try:
                validator.assert_error_structure(response.json())
            except ValueError:
                assert response.status_code == 400


@allure.feature("Orders API")
@allure.story("Get Order")
class TestGetOrder:
    
    def test_get_order_success(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create an order first"):
            order_id, _ = test_helpers.create_test_order(amount=2000.0, currency='KZT')
        
        with allure.step("Get order by ID"):
            response, execution_time = api_client.get_order(order_id)
        
        with allure.step("Verify status code is 200"):
            validator.assert_status_code(response, 200)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify response structure"):
            data = response.json()
            validator.assert_json_structure(data, ['id', 'amount', 'currency', 'status', 'created_at'])
        
        with allure.step("Verify order ID matches"):
            validator.assert_field_value(data, 'id', order_id)
    
    def test_get_order_not_found(self, api_client, validator, mock_server):
        with allure.step("Get non-existent order"):
            response, execution_time = api_client.get_order('order_nonexistent_999')
        
        with allure.step("Verify status code is 404"):
            validator.assert_status_code(response, 404)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'NOT_FOUND')
    
    def test_get_order_invalid_id_format(self, api_client, validator, mock_server):
        with allure.step("Get order with invalid ID"):
            response, execution_time = api_client.get_order('invalid_id_123')
        
        with allure.step("Verify status code is 404"):
            validator.assert_status_code(response, 404)
