import allure
from utils.config import config
from utils.validators import ResponseValidator


@allure.feature("Payments API")
@allure.story("Create Payment")
class TestCreatePayment:
    
    def test_create_payment_success(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create an order first"):
            order_id, _ = test_helpers.create_test_order(amount=3000.0, currency='KZT')
        
        with allure.step("Create payment for the order"):
            response, execution_time = api_client.create_payment(order_id, payment_method='card')
        
        with allure.step("Verify status code is 201"):
            validator.assert_status_code(response, 201)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify response structure"):
            data = response.json()
            validator.assert_json_structure(
                data,
                ['id', 'order_id', 'amount', 'currency', 'status', 'created_at', 'payment_method']
            )
        
        with allure.step("Verify payment values"):
            validator.assert_field_value(data, 'order_id', order_id)
            validator.assert_field_value(data, 'amount', 3000.0)
            validator.assert_field_value(data, 'status', 'pending')
            validator.assert_field_starts_with(data, 'id', 'payment_')
    
    def test_create_payment_order_not_found(self, api_client, validator, mock_server):
        with allure.step("Create payment for non-existent order"):
            response, execution_time = api_client.create_payment('order_nonexistent_999')
        
        with allure.step("Verify status code is 404"):
            validator.assert_status_code(response, 404)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'NOT_FOUND')


@allure.feature("Payments API")
@allure.story("Get Payment")
class TestGetPayment:
    
    def test_get_payment_success(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create order and payment"):
            order_id, payment_id, _, _ = test_helpers.create_order_and_payment(
                amount=4000.0, currency='KZT'
            )
        
        with allure.step("Get payment by ID"):
            response, execution_time = api_client.get_payment(payment_id)
        
        with allure.step("Verify status code is 200"):
            validator.assert_status_code(response, 200)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify response structure"):
            data = response.json()
            validator.assert_json_structure(
                data,
                ['id', 'order_id', 'amount', 'currency', 'status', 'created_at']
            )
        
        with allure.step("Verify payment ID matches"):
            validator.assert_field_value(data, 'id', payment_id)
    
    def test_get_payment_not_found(self, api_client, validator, mock_server):
        with allure.step("Get non-existent payment"):
            response, execution_time = api_client.get_payment('payment_nonexistent_999')
        
        with allure.step("Verify status code is 404"):
            validator.assert_status_code(response, 404)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'NOT_FOUND')


@allure.feature("Payments API")
@allure.story("Refund Payment")
class TestRefundPayment:
    
    def test_refund_payment_success(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create order and payment"):
            _, payment_id, _, _ = test_helpers.create_order_and_payment(
                amount=5000.0, currency='KZT'
            )
        
        with allure.step("Refund the payment"):
            response, execution_time = api_client.refund_payment(payment_id)
        
        with allure.step("Verify status code is 201"):
            validator.assert_status_code(response, 201)
        
        with allure.step("Verify response time"):
            validator.assert_response_time(execution_time, config.max_response_time_ms)
        
        with allure.step("Verify response structure"):
            data = response.json()
            validator.assert_json_structure(
                data,
                ['id', 'payment_id', 'amount', 'currency', 'status', 'created_at']
            )
        
        with allure.step("Verify refund values"):
            validator.assert_field_value(data, 'payment_id', payment_id)
            validator.assert_field_value(data, 'status', 'completed')
            validator.assert_field_starts_with(data, 'id', 'refund_')
    
    def test_refund_payment_partial(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create order and payment"):
            _, payment_id, _, _ = test_helpers.create_order_and_payment(
                amount=6000.0, currency='KZT'
            )
        
        with allure.step("Refund partial amount"):
            response, execution_time = api_client.refund_payment(payment_id, amount=3000.0)
        
        with allure.step("Verify status code is 201"):
            validator.assert_status_code(response, 201)
        
        with allure.step("Verify refund amount"):
            validator.assert_field_value(response.json(), 'amount', 3000.0)
    
    def test_refund_payment_not_found(self, api_client, validator, mock_server):
        with allure.step("Refund non-existent payment"):
            response, execution_time = api_client.refund_payment('payment_nonexistent_999')
        
        with allure.step("Verify status code is 404"):
            validator.assert_status_code(response, 404)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'NOT_FOUND')
    
    def test_refund_payment_exceeds_amount(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create order and payment"):
            _, payment_id, _, _ = test_helpers.create_order_and_payment(
                amount=1000.0, currency='KZT'
            )
        
        with allure.step("Try to refund more than payment amount"):
            response, execution_time = api_client.refund_payment(payment_id, amount=2000.0)
        
        with allure.step("Verify status code is 400"):
            validator.assert_status_code(response, 400)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'VALIDATION_ERROR')
    
    def test_refund_already_refunded_payment(self, api_client, validator, test_helpers, mock_server):
        with allure.step("Create order and payment"):
            _, payment_id, _, _ = test_helpers.create_order_and_payment(
                amount=2000.0, currency='KZT'
            )
        
        with allure.step("Refund payment first time"):
            refund_response, _ = api_client.refund_payment(payment_id)
            validator.assert_status_code(refund_response, 201)
        
        with allure.step("Try to refund again"):
            response, execution_time = api_client.refund_payment(payment_id)
        
        with allure.step("Verify status code is 400"):
            validator.assert_status_code(response, 400)
        
        with allure.step("Verify error structure"):
            validator.assert_error_structure(response.json(), 'INVALID_STATUS')
