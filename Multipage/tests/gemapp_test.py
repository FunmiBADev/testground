import unittest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
import os
import json
from app import get_platform_token, find_jre, parse_jre_version, fetch_and_update_data

class TestGetPlatformToken(unittest.TestCase):

  @patch('requests.post')  # Mock the requests.post function
  def test_successful_login(self, mock_post):
    mock_response = Mock()
    mock_response.headers = {'Set-Cookie': 'platform_token=abc123'}
    mock_post.return_value = mock_response

    token = get_platform_token('https://api.example.com/', 'username', 'password')

    self.assertEqual(token, 'platform_token=abc123')
    mock_post.assert_called_once_with('https://api.example.com/PLATFORM_API_LOGIN', auth=('username', 'password'))

  @patch('requests.post')  # Mock the requests.post function
  def test_login_failure(self, mock_post):
    mock_response = Mock()
    mock_response.headers = {}  # No platform_token in cookies
    mock_post.return_value = mock_response

    token = get_platform_token('https://api.example.com/', 'username', 'password')

    self.assertEqual(token, '')
    mock_post.assert_called_once_with('https://api.example.com/PLATFORM_API_LOGIN', auth=('username', 'password'))

  @patch('requests.post')  # Mock the requests.post function
  def test_login_exception(self, mock_post):
    mock_post.side_effect = Exception('Connection error')

    with self.assertRaises(Exception):
      get_platform_token('https://api.example.com/', 'username', 'password')

    mock_post.assert_called_once_with('https://api.example.com/PLATFORM_API_LOGIN', auth=('username', 'password'))
import unittest

class TestFindJre(unittest.TestCase):

  def test_jre_in_assembly(self):
    assemblies = [
      {'name': 'oracle.jdk:17.0.4'},
      {'name': 'some-other-assembly'},
    ]
    variables = []
    start_cmd = 'some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    self.assertEqual(jre_info, 'ASSEMBLY = oracle.jdk:17.0.4')
    self.assertEqual(env_var_count, 0)

  def test_jre_in_env_variable(self):
    assemblies = []
    variables = [
      {'value': 'JAVA_11_HOME=/usr/lib/jvm/java-11-openjdk'},
    ]
    start_cmd = 'some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    self.assertEqual(jre_info, 'ENV_VARIABLE = JAVA_11_HOME=/usr/lib/jvm/java-11-openjdk')
    self.assertEqual(env_var_count, 1)

  def test_jre_in_start_cmd(self):
    assemblies = []
    variables = []
    start_cmd = 'JAVA_17_HOME=/usr/lib/jvm/java-17-openjdk some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    self.assertEqual(jre_info, 'START_CMD = JAVA_17_HOME=/usr/lib/jvm/java-17-openjdk some_command')
    self.assertEqual(env_var_count, 0)

  def test_no_jre_found(self):
    assemblies = [
      {'name': 'some-other-assembly'},
    ]
    variables = []
    start_cmd = 'some_command'

    jre_info, env_var_count = find_jre(assemblies, variables, start_cmd)

    self.assertEqual(jre_info, '')
    self.assertEqual(env_var_count, 0)
