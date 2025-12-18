import pytest
import subprocess
import time
import requests
from utils.config import config


@pytest.fixture(scope="session")
def mock_server():
    import sys
    import os
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    mock_server_path = project_root / "mock_server.py"
    
    server_process = subprocess.Popen(
        [sys.executable, str(mock_server_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(project_root),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
    )
    
    max_attempts = 30
    server_ready = False
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{config.api_base_url}/health", timeout=2)
            if response.status_code == 200:
                server_ready = True
                break
        except Exception:
            time.sleep(0.5)
    
    if not server_ready:
        try:
            stdout, stderr = server_process.communicate(timeout=1)
            error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Unknown error"
        except:
            error_msg = "Could not get error details"
        server_process.terminate()
        server_process.wait()
        pytest.fail(f"Mock server failed to start after {max_attempts} attempts. Error: {error_msg}")
    
    yield
    
    server_process.terminate()
    server_process.wait()


@pytest.fixture
def api_client():
    from utils.api_client import APIClient
    return APIClient()


@pytest.fixture
def validator():
    from utils.validators import ResponseValidator
    return ResponseValidator()


@pytest.fixture
def test_helpers(api_client, validator):
    from utils.test_helpers import TestHelpers
    return TestHelpers(api_client, validator)

