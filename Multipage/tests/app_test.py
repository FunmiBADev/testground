import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
import os
import json
from app import get_platform_token, find_jre, parse_jre_version, fetch_and_update_data

# Load configs and APIs
configs_dir = 'configs/'
with open(os.path.join(configs_dir, 'config.json')) as config_file:
    config = json.load(config_file)
platform_tags = config['platform_tags']

with open(os.path.join(configs_dir, 'apis.json')) as apis_file:
    apis = json.load(apis_file)

class TestAppFunctions(unittest.TestCase):

    @patch('requests.post')
    def test_get_platform_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.headers = {
            'Set-Cookie': 'platform_token=mock_token; Path=/; HttpOnly'
        }
        mock_post.return_value = mock_response
        
        token = get_platform_token('http://mockplatform.com', 'username', 'password')
        self.assertEqual(token, 'platform_token=mock_token')

    def test_find_jre(self):
        assemblies = [{'name': 'jre-11', 'version': '11.0.2'}]
        variables = [{'value': 'JAVA_11_HOME=/path/to/java11'}]
        start_cmd = 'JAVA_11'
        
        jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)
        self.assertIn('ASSEMBLY = jre-11=11.0.2', jre_info)
        self.assertIn('ENV_VARIABLE = JAVA_11_HOME=/path/to/java11', jre_info)
        self.assertIn('START_CMD = JAVA_11', jre_info)
        self.assertEqual(env_var_count, 1)

    def test_parse_jre_version(self):
        jre_string = "ASSEMBLY = jre-11=11.0.2 ENV_VARIABLE = JAVA_11_HOME=/path/to/java11 START_CMD = JAVA_11"
        version = parse_jre_version(jre_string)
        self.assertEqual(version, '11.0.2')

    @patch('requests.get')
    @patch('your_app.get_platform_token')
    def test_fetch_and_update_data(self, mock_get_platform_token, mock_get):
        mock_get_platform_token.return_value = 'mock_token'
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'name': 'process1', 'host': 'host1', 'assemblies': [{'name': 'jre-17', 'version': '17.0.1'}], 'variables': [], 'startCmd': ''}
        ]
        mock_get.return_value = mock_response
        
        fetch_and_update_data()
        
        self.assertFalse(combined_df.empty)
        self.assertIn('jre_version', combined_df.columns)
        self.assertIn('green_jres', combined_df.columns)
        self.assertIn('eol_jres', combined_df.columns)
        self.assertEqual(combined_df['green_jres'].iloc[0], '17.0.1')

if __name__ == '__main__':
    unittest.main()

# python -m unittest discover -s tests
