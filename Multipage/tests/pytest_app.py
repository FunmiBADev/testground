import pytest
from unittest.mock import patch, mock_open, MagicMock
import requests
import json
import pandas as pd
from your_module import (
    get_platform_token,
    find_jre,
    parse_jre_version,
    fetch_and_update_data,
    combined_df
)

# Sample data for testing
platform_tags = [
    {
        "url": "https://platform1.example.com",
        "tag": "platform1",
        "tag_name": "Platform 1"
    }
]

apis = {
    "PLATFORM_API_LOGIN": "/login",
    "PLATFORM_API_PROCESS_DEFINITIONS": "/process_definitions",
    "PLATFORM_API_JRE": "/jre"
}

username = 'testUser'
password = 'testPass'

# Mock environment variables
@patch.dict(os.environ, {'PASSWORD': password})
def test_get_platform_token():
    platform_endpoint = "https://platform1.example.com"

    with patch('requests.post') as mock_post:
        mock_post.return_value.headers = {'Set-Cookie': 'platform_token=abc123; Path=/'}
        token = get_platform_token(platform_endpoint, username, password)
        assert token == 'platform_token=abc123'

        mock_post.return_value.headers = {}
        token = get_platform_token(platform_endpoint, username, password)
        assert token == ''

def test_find_jre():
    assemblies = [
        {'name': 'jre_1', 'version': '1.8.0_351'},
        {'name': 'other_assembly', 'version': '2.0.0'},
        {'name': 'jre_2', 'version': '1.8.0_352'}
    ]

    variables = [
        {'name': 'VAR1', 'value': 'JAVA_8_HOME'},
        {'name': 'VAR2', 'value': None},
        {'name': 'VAR3', 'value': 'OTHER_VALUE'}
    ]

    start_cmd = 'run -Djava.version=JAVA_8'
    expected_output = (
        'ASSEMBLY = jre_1=1.8.0_351 ASSEMBLY = jre_2=1.8.0_352 '
        'ENV_VARIABLE = JAVA_8_HOME '
        'START_CMD = run -Djava.version=JAVA_8'
    )
    result = find_jre(assemblies, variables, start_cmd)
    assert result == expected_output

def test_parse_jre_version():
    jre_string = 'ASSEMBLY = jre_1=1.8.0_351 ASSEMBLY = jre_2=1.8.0_352'
    result = parse_jre_version(jre_string)
    assert result == '1.8.0_352'

    jre_string = 'ENV_VARIABLE = JAVA_8_HOME'
    result = parse_jre_version(jre_string)
    assert result == 'JAVA_8_HOME'

    jre_string = 'START_CMD = run -Djava.version=JAVA_8'
    result = parse_jre_version(jre_string)
    assert result == ' run -Djava.version=JAVA_8'

    jre_string = 'NO_MATCHING_PATTERN'
    result = parse_jre_version(jre_string)
    assert result is None

@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"platform_tags": platform_tags}))
@patch('requests.get')
@patch('requests.post')
@patch('pandas.DataFrame.apply')
def test_fetch_and_update_data(mock_apply, mock_post, mock_get, mock_open):
    mock_post.return_value.headers = {'Set-Cookie': 'platform_token=abc123; Path=/'}
    mock_get.return_value.json.return_value = [{
        'assemblies': [{'name': 'jre_1', 'version': '1.8.0_351'}],
        'variables': [{'name': 'VAR1', 'value': 'JAVA_8_HOME'}],
        'startCmd': 'run -Djava.version=JAVA_8',
        'name': 'Process 1',
        'host': 'host1'
    }]
    mock_apply.side_effect = lambda func, axis, result_type: pd.DataFrame([['ASSEMBLY = jre_1=1.8.0_351 ENV_VARIABLE = JAVA_8_HOME START_CMD = run -Djava.version=JAVA_8', None]])

    fetch_and_update_data()

    assert not combined_df.empty
    assert 'name' in combined_df.columns
    assert 'host' in combined_df.columns
    assert 'jre' in combined_df.columns
    assert 'jre_version' in combined_df.columns
    assert 'green_jres' in combined_df.columns
    assert 'eol_jres' in combined_df.columns
    assert 'env_var_cmd' in combined_df.columns

if __name__ == '__main__':
    pytest.main()
