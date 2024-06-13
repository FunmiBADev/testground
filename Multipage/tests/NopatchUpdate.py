import pytest
import pandas as pd
import json
from unittest.mock import MagicMock

# Import the function to be tested
from main import fetch_and_update_data, combined_df

# Mocked data for platform definitions
mock_platform_defs = json.dumps([
    {
        'name': 'test_name',
        'host': 'test_host',
        'assemblies': [{'name': 'jre-8u292', 'version': '8.0.292'}],
        'variables': [{'name': 'JAVA_HOME', 'value': '/usr/lib/jvm/java-8-openjdk-amd64'}],
        'startCmd': 'java -version'
    }
])

# Mocking the requests.get response
mock_response = MagicMock()
mock_response.json.return_value = json.loads(mock_platform_defs)

# Mock for requests module
class MockRequestsResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@pytest.fixture
def platform_tags(monkeypatch):
    # Mock platform_tags as per your needs
    return [
        {"tag": "AA42557", "tag_name": "PLATFORM", "url": "https://www.platform.com"},
        {"tag": "AA34475", "tag_name": "PLATFORM_ONE", "url": "https://www.platformone.com"}
    ]

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('PASSWORD', 'test_password')
    monkeypatch.setenv('PASSUAT', 'uat_password')

def test_fetch_and_update_data(platform_tags, mock_env_vars, monkeypatch):
    monkeypatch.setattr('requests.get', lambda url, headers: MockRequestsResponse(json.loads(mock_platform_defs), 200))

    fetch_and_update_data()

    expected_data = {
        'name': ['test_name'],
        'host': ['test_host'],
        'jre': ['ASSEMBLY = jre-8u292=8.0.292 ENV_VARIABLE = /usr/lib/jvm/java-8-openjdk-amd64 START_CMD = java -version'],
        'jre_version': ['8.0.292'],
        'platform_tag': ['AA42557'],
        'green_jres': [None],
        'eol_jres': [None],
        'env_var_cmd': [None]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(combined_df, expected_df)

if __name__ == '__main__':
    pytest.main()
