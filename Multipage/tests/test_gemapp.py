import requests  # Don't mock for actual network interaction
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import os
import json
from datetime import datetime
from app import get_platform_token, find_jre, parse_jre_version, fetch_and_update_data

def test_get_platform_token_successful_login(username, password):
    platform_endpoint = 'https://api.example.com/'
    response = requests.post(f'{platform_endpoint}{PLATFORM_API_LOGIN}', auth=(username, password))
    for header in response.headers['Set-Cookie'].split(';'):
        if header.startswith('platform_token'):
            return

    assert False, 'Platform token not found in response'

def test_get_platform_token_login_failure(username, password):
    platform_endpoint = 'https://api.example.com/'
    response = requests.post(f'{platform_endpoint}{PLATFORM_API_LOGIN}', auth=(username, password))
    assert not 'platform_token' in response.headers

def test_get_platform_token_login_exception(username, password):
    platform_endpoint = 'https://api.example.com/'
    with pytest.raises(Exception):
        requests.post(f'{platform_endpoint}{PLATFORM_API_LOGIN}', auth=(username, password))

def test_find_jre_assembly():
    assemblies = [
        {'name': 'oracle.jdk:17.0.4'},
        {'name': 'some-other-assembly'},
    ]
    variables = []
    start_cmd = 'some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    assert jre_info == 'ASSEMBLY = oracle.jdk:17.0.4'
    assert env_var_count == 0

def test_find_jre_env_variable():
    assemblies = []
    variables = [
        {'value': 'JAVA_11_HOME=/usr/lib/jvm/java-11-openjdk'},
    ]
    start_cmd = 'some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    assert jre_info == 'ENV_VARIABLE = JAVA_11_HOME=/usr/lib/jvm/java-11-openjdk'
    assert env_var_count == 1

def test_find_jre_start_cmd():
    assemblies = []
    variables = []
    start_cmd = 'JAVA_17_HOME=/usr/lib/jvm/java-17-openjdk some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    assert jre_info == 'START_CMD = JAVA_17_HOME=/usr/lib/jvm/java-17-openjdk some_command'
    assert env_var_count == 0

def test_find_jre_no_jre_found():
    assemblies = [
        {'name': 'some-other-assembly'},
    ]
    variables = []
    start_cmd = 'some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    assert jre_info == ''
    assert env_var_count == 0

def test_parse_jre_version_assembly():
    jre_string = 'ASSEMBLY = oracle.jdk:17.0.4'
    version = parse_jre_version(jre_string)
    assert version == '17.0.4'

def test_parse_jre_version_env_variable():
    jre_string = 'ENV_VARIABLE = JAVA_11_HOME=/usr/lib/jvm/java-11-openjdk'
    version = parse_jre_version(jre_string)
    assert version == '11'

def test_parse_jre_version_start_cmd():
    jre_string = 'START_CMD = JAVA_17_HOME=/usr/lib/jvm/java-17-openjdk some_command'
    version = parse_jre_version(jre_string)
    assert version == '17'

def test_parse_jre_version_no_jre_info():
    jre_string = ''  # Empty string indicating no JRE info
    version = parse_jre_version(jre_string)
    assert version is None  # Should return None if no JRE version found
    


@pytest.fixture
def mock_requests_get(monkeypatch):
    mock_get = MagicMock()
    monkeypatch.setattr(requests, 'get', mock_get)
    return mock_get

def test_fetch_and_update_data_success(mock_requests_get, platform_tags):
    # Mock successful responses with expected data
    mock_responses = []
    for stats in platform_tags:
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'name': 'process1', 'assemblies': [], 'variables': [], 'startCmd': None},
            {'name': 'process2', 'assemblies': [{'name': 'oracle.jdk:11.0.15'}], 'variables': [], 'startCmd': None},
        ]
        mock_responses.append(mock_response)
    mock_requests_get.side_effect = mock_responses

    # Call the function and assert results
    fetch_and_update_data()

    assert combined_df.shape[0] == 4  # 2 processes from each platform tag
    assert 'jre' in combined_df.columns
    assert 'env_var_count' in combined_df.columns

def test_fetch_and_update_data_login_failure(mock_requests_get, platform_tags):
    # Mock failed login (empty response)
    mock_requests_get.return_value = MagicMock()
    mock_requests_get.return_value.json.return_value = []

    with pytest.raises(Exception):
        fetch_and_update_data()

def test_fetch_and_update_data_request_exception(mock_requests_get, platform_tags):
    # Mock request exception
    mock_requests_get.side_effect = Exception('Connection error')

    with pytest.raises(Exception):
        fetch_and_update_data()

# Assuming platform_tags is a defined list/dictionary used in fetch_and_update_data
@pytest.mark.skipif(platform_tags is None, reason="platform_tags fixture not defined")
def test_fetch_and_update_data(mock_requests_get):
    # Run the test with the actual platform_tags fixture
    test_fetch_and_update_data_success(mock_requests_get, platform_tags)

