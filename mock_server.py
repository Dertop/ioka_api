from flask import Flask, jsonify
from mock_server.constants import (
    ORDER_STATUS_PENDING,
    PAYMENT_STATUS_PENDING,
    PAYMENT_STATUS_REFUNDED,
    REFUND_STATUS_COMPLETED,
    DEFAULT_CURRENCY,
    DEFAULT_PAYMENT_METHOD,
    get_current_timestamp
)
from mock_server.helpers import (
    simulate_processing_time,
    create_not_found_response,
    create_validation_error,
    create_invalid_request_error,
    create_invalid_status_error,
    parse_request_json
)

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

orders_db = {}
payments_db = {}
order_counter = 1
payment_counter = 1


@app.route('/orders', methods=['POST'])
def create_order():
    global order_counter
    
    data = parse_request_json(force=True)
    
    if not data:
        return create_invalid_request_error("Request body is required")
    
    if 'amount' not in data or 'currency' not in data:
        return create_validation_error("amount and currency are required")
    
    if data.get('amount', 0) <= 0:
        return create_validation_error("amount must be greater than 0")
    
    simulate_processing_time()
    
    order_id = f"order_{order_counter}"
    order_counter += 1
    
    order = {
        "id": order_id,
        "amount": data['amount'],
        "currency": data.get('currency', DEFAULT_CURRENCY),
        "status": ORDER_STATUS_PENDING,
        "created_at": get_current_timestamp(),
        "description": data.get('description', ''),
        "customer": data.get('customer', {})
    }
    
    orders_db[order_id] = order
    return jsonify(order), 201


@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    simulate_processing_time()
    
    if order_id not in orders_db:
        return create_not_found_response("Order", order_id)
    
    return jsonify(orders_db[order_id]), 200


@app.route('/orders/<order_id>/payments', methods=['POST'])
def create_payment(order_id):
    global payment_counter
    
    simulate_processing_time()
    
    if order_id not in orders_db:
        return create_not_found_response("Order", order_id)
    
    data = parse_request_json()
    
    payment_id = f"payment_{payment_counter}"
    payment_counter += 1
    
    order = orders_db[order_id]
    payment = {
        "id": payment_id,
        "order_id": order_id,
        "amount": order['amount'],
        "currency": order['currency'],
        "status": PAYMENT_STATUS_PENDING,
        "created_at": get_current_timestamp(),
        "payment_method": data.get('payment_method', DEFAULT_PAYMENT_METHOD) if data else DEFAULT_PAYMENT_METHOD
    }
    
    payments_db[payment_id] = payment
    return jsonify(payment), 201


@app.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    simulate_processing_time()
    
    if payment_id not in payments_db:
        return create_not_found_response("Payment", payment_id)
    
    return jsonify(payments_db[payment_id]), 200


@app.route('/payments/<payment_id>/refund', methods=['POST'])
def refund_payment(payment_id):
    simulate_processing_time()
    
    if payment_id not in payments_db:
        return create_not_found_response("Payment", payment_id)
    
    payment = payments_db[payment_id]
    
    if payment['status'] == PAYMENT_STATUS_REFUNDED:
        return create_invalid_status_error("Payment already refunded")
    
    data = parse_request_json()
    refund_amount = data.get('amount', payment['amount']) if data else payment['amount']
    
    if refund_amount > payment['amount']:
        return create_validation_error("Refund amount cannot exceed payment amount")
    
    payment['status'] = PAYMENT_STATUS_REFUNDED
    payment['refunded_amount'] = refund_amount
    payment['refunded_at'] = get_current_timestamp()
    
    refund = {
        "id": f"refund_{payment_id}",
        "payment_id": payment_id,
        "amount": refund_amount,
        "currency": payment['currency'],
        "status": REFUND_STATUS_COMPLETED,
        "created_at": get_current_timestamp()
    }
    
    return jsonify(refund), 201


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
