import pytest
from unittest.mock import patch, MagicMock
import os
import json
import requests
import pandas as pd

from main import Config, __get_password, get_platform_token, find_jre, parse_jre_version, fetch_and_update_data, combined_df

class TestConfig:
    def setup_method(self):
        self.config = Config()

    def test_get_platform_tags(self):
        expected_tags = [
            {"tag": "AA42557", "tag_name": "PLATFORM", "url": "https://www.platform.com"},
            {"tag": "AA34475", "tag_name": "PLATFORM_ONE", "url": "https://www.platformone.com"},
            {"tag": "AA45492", "tag_name": "PLATFORM_TWO", "url": "https://www.platformtwo.com"}
        ]
        assert self.config.get_platform_tags() == expected_tags

    def test_get_apis(self):
        expected_apis = {
            "PLATFORM_API_LOGIN": "/api/login",
            "PLATFORM_API_PROCESS_DEFINITIONS": "/api/proc/definitions",
            "PLATFORM_API_JRE": "/api/jre/display"
        }
        assert self.config.get_apis() == expected_apis

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('PASSWORD', 'test_password')
    monkeypatch.setenv('PASSUAT', 'uat_password')

@pytest.fixture
def platform_tags():
    return [
        {"tag": "AA42557", "tag_name": "PLATFORM", "url": "https://www.platform.com"},
        {"tag": "UAT", "tag_name": "UAT_PLATFORM", "url": "https://www.uatplatform.com"}
    ]

def test___get_password(mock_env_vars, platform_tags):
    with patch('main.platform_tags', platform_tags):
        assert __get_password("PLATFORM") == "test_password"
        assert __get_password("UAT_PLATFORM") == "uat_password"

@patch('requests.post')
def test_get_platform_token(mock_post):
    mock_response = MagicMock()
    mock_response.headers = {'Set-Cookie': 'platform_token=abcd1234; Path=/'}
    mock_post.return_value = mock_response

    assert get_platform_token("https://www.platform.com", "testUser", "PLATFORM") == 'platform_token=abcd1234'

def test_find_jre():
    assemblies = [{'name': 'jre-8u292', 'version': '8.0.292'}]
    variables = [{'name': 'JAVA_HOME', 'value': '/usr/lib/jvm/java-8-openjdk-amd64'}]
    start_cmd = "java -version"

    expected_jre_info = "ASSEMBLY = jre-8u292=8.0.292 ENV_VARIABLE = /usr/lib/jvm/java-8-openjdk-amd64 START_CMD = java -version"
    assert find_jre(assemblies, variables, start_cmd) == expected_jre_info

def test_parse_jre_version():
    assert parse_jre_version("ASSEMBLY = jre-8u292=8.0.292") == "8.0.292"
    assert parse_jre_version("ENV_VARIABLE = /usr/lib/jvm/java-8-openjdk-amd64") == "/usr/lib/jvm/java-8-openjdk-amd64"
    assert parse_jre_version("START_CMD = java -version") == " java -version"

@patch('requests.get')
@patch('main.get_platform_token')
def test_fetch_and_update_data(mock_get_platform_token, mock_get):
    mock_get_platform_token.return_value = "platform_token=abcd1234"

    platform_defs_json = json.dumps([
        {'name': 'test_name', 'host': 'test_host', 'assemblies': [{'name': 'jre-8u292', 'version': '8.0.292'}], 'variables': [{'name': 'JAVA_HOME', 'value': '/usr/lib/jvm/java-8-openjdk-amd64'}], 'startCmd': 'java -version'}
    ])
    mock_response = MagicMock()
    mock_response.json.return_value = json.loads(platform_defs_json)
    mock_get.return_value = mock_response

    fetch_and_update_data()

    expected_data = {
        'name': ['test_name'],
        'host': ['test_host'],
        'jre': ['ASSEMBLY = jre-8u292=8.0.292 ENV_VARIABLE = /usr/lib/jvm/java-8-openjdk-amd64 START_CMD = java -version'],
        'env_var_count': [''],
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
