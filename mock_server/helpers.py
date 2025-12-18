from flask import jsonify
from typing import Dict, Any, Optional
import time
import random
from mock_server.constants import (
    MIN_PROCESSING_TIME,
    MAX_PROCESSING_TIME,
    ERROR_INVALID_REQUEST,
    ERROR_VALIDATION_ERROR,
    ERROR_NOT_FOUND,
    ERROR_INVALID_STATUS
)


def simulate_processing_time() -> None:
    time.sleep(random.uniform(MIN_PROCESSING_TIME, MAX_PROCESSING_TIME))


def create_error_response(code: str, message: str, status_code: int = 400) -> tuple:
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), status_code


def create_not_found_response(resource_type: str, resource_id: str) -> tuple:
    return create_error_response(
        ERROR_NOT_FOUND,
        f"{resource_type} {resource_id} not found",
        404
    )


def create_validation_error(message: str) -> tuple:
    return create_error_response(ERROR_VALIDATION_ERROR, message, 400)


def create_invalid_request_error(message: str) -> tuple:
    return create_error_response(ERROR_INVALID_REQUEST, message, 400)


def create_invalid_status_error(message: str) -> tuple:
    return create_error_response(ERROR_INVALID_STATUS, message, 400)


def parse_request_json(force: bool = False) -> Optional[Dict[str, Any]]:
    from flask import request
    
    try:
        if force:
            return request.get_json(force=True) if request.data else None
        return request.get_json() or None
    except Exception:
        return None

