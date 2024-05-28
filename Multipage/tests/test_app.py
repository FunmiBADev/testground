import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import json
from datetime import datetime
from app import get_platform_token, find_jre, parse_jre_version, fetch_and_update_data

# Load configs and APIs
configs_dir = 'configs/'
with open(os.path.join(configs_dir, 'config.json')) as config_file:
    config = json.load(config_file)
platform_tags = config['platform_tags']

with open(os.path.join(configs_dir, 'apis.json')) as apis_file:
    apis = json.load(apis_file)

# Mock global combined_df for testing fetch_and_update_data
combined_df = pd.DataFrame()

@pytest.fixture
def mock_post():
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_get():
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_get_platform_token():
    with patch('your_app.get_platform_token') as mock_get_platform_token:
        yield mock_get_platform_token

def test_get_platform_token(mock_post):
    mock_response = MagicMock()
    mock_response.headers = {
        'Set-Cookie': 'platform_token=mock_token; Path=/; HttpOnly'
    }
    mock_post.return_value = mock_response
    
    token = get_platform_token('http://mockplatform.com', 'username', 'password')
    assert token == 'platform_token=mock_token'

def test_find_jre():
    assemblies = [{'name': 'jre-11', 'version': '11.0.2'}]
    variables = [{'value': 'JAVA_11_HOME=/path/to/java11'}]
    start_cmd = 'JAVA_11'
    
    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)
    assert 'ASSEMBLY = jre-11=11.0.2' in jre_info
    assert 'ENV_VARIABLE = JAVA_11_HOME=/path/to/java11' in jre_info
    assert 'START_CMD = JAVA_11' in jre_info
    assert env_var_count == 1

def test_parse_jre_version():
    jre_string = "ASSEMBLY = jre-11=11.0.2 ENV_VARIABLE = JAVA_11_HOME=/path/to/java11 START_CMD = JAVA_11"
    version = parse_jre_version(jre_string)
    assert version == '11.0.2'

def test_fetch_and_update_data(mock_get, mock_get_platform_token):
    mock_get_platform_token.return_value = 'mock_token'
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {'name': 'process1', 'host': 'host1', 'assemblies': [{'name': 'jre-17', 'version': '17.0.1'}], 'variables': [], 'startCmd': ''}
    ]
    mock_get.return_value = mock_response
    
    fetch_and_update_data()
    
    global combined_df
    assert not combined_df.empty
    assert 'jre_version' in combined_df.columns
    assert 'green_jres' in combined_df.columns
    assert 'eol_jres' in combined_df.columns
    assert combined_df['green_jres'].iloc[0] == '17.0.1'

