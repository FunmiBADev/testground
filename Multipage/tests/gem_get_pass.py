import os
import pytest
from unittest.mock import patch

from logic.main import getUsernameAndPassword


@pytest.fixture
def env_vars():
    with patch.dict(os.environ, {
        'PROD_USERNAME': 'demo_your_prod_username',
        'PASS_PROD': 'demo_your_prod_password',
        'UAT_USERNAME': 'demo_your_uat_username',
        'PASS_UAT': 'demo_your_uat_password'
    }):
        yield


def test_get_username_and_password_prod(env_vars):
    platform_tag = 'PROD'
    expected_username = 'demo_your_prod_username'
    expected_password = 'demo_your_prod_password'

    username, password = getUsernameAndPassword(platform_tag)
    assert username == expected_username
    assert password == expected_password

def test_get_username_and_password_uat(env_vars):
    platform_tag = 'UAT'
    expected_username = 'demo_your_uat_username'
    expected_password = 'demo_your_uat_password'

    username, password = getUsernameAndPassword(platform_tag)
    assert username == expected_username
    assert password == expected_password
