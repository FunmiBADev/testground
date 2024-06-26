import os
import pytest
from unittest.mock import patch

from logic.main import getUsernameAndPassword  # Correct import statement

# Example environment variables to be used in the tests
PROD_USERNAME = 'demo_your_prod_username'
PASS_PROD = 'demo_your_prod_password'
UAT_USERNAME = 'demo_your_uat_username'
PASS_UAT = 'demo_your_uat_password'

def test_get_username_and_password_prod():
    platform_tag = 'PROD'
    expected_username = PROD_USERNAME
    expected_password = PASS_PROD

    with patch.dict(os.environ, {
        'PROD_USERNAME': PROD_USERNAME,
        'PASS_PROD': PASS_PROD,
        'UAT_USERNAME': UAT_USERNAME,
        'PASS_UAT': PASS_UAT
    }):
        username, password = getUsernameAndPassword(platform_tag)
        assert username == expected_username
        assert password == expected_password

def test_get_username_and_password_uat():
    platform_tag = 'UAT'
    expected_username = UAT_USERNAME
    expected_password = PASS_UAT

    with patch.dict(os.environ, {
        'PROD_USERNAME': PROD_USERNAME,
        'PASS_PROD': PASS_PROD,
        'UAT_USERNAME': UAT_USERNAME,
        'PASS_UAT': PASS_UAT
    }):
        username, password = getUsernameAndPassword(platform_tag)
        assert username == expected_username
        assert password == expected_password

# Additional tests to cover edge cases
def test_get_username_and_password_mixed_case_prod():
    platform_tag = 'prod'
    expected_username = PROD_USERNAME
    expected_password = PASS_PROD

    with patch.dict(os.environ, {
        'PROD_USERNAME': PROD_USERNAME,
        'PASS_PROD': PASS_PROD,
        'UAT_USERNAME': UAT_USERNAME,
        'PASS_UAT': PASS_UAT
    }):
        username, password = getUsernameAndPassword(platform_tag.upper())
        assert username == expected_username
        assert password == expected_password

def test_get_username_and_password_mixed_case_uat():
    platform_tag = 'uat'
    expected_username = UAT_USERNAME
    expected_password = PASS_UAT

    with patch.dict(os.environ, {
        'PROD_USERNAME': PROD_USERNAME,
        'PASS_PROD': PASS_PROD,
        'UAT_USERNAME': UAT_USERNAME,
        'PASS_UAT': PASS_UAT
    }):
        username, password = getUsernameAndPassword(platform_tag.upper())
        assert username == expected_username
        assert password == expected_password

if __name__ == "__main__":
    pytest.main()


### Add on

# Load the test environment variables from the .env.test file
load_dotenv('.env.test')

@pytest.fixture(scope='module', autouse=True)
def set_env_vars():
    # Patch the environment variables for the duration of the tests
    with patch.dict(os.environ, {
        'PROD_USERNAME': os.getenv('PROD_USERNAME'),
        'PASS_PROD': os.getenv('PASS_PROD'),
        'UAT_USERNAME': os.getenv('UAT_USERNAME'),
        'PASS_UAT': os.getenv('PASS_UAT')
    }):
        yield

@pytest.mark.parametrize("platform_tag, expected_username, expected_password", [
    ('PROD', os.getenv('PROD_USERNAME'), os.getenv('PASS_PROD')),
    ('UAT', os.getenv('UAT_USERNAME'), os.getenv('PASS_UAT')),
    ('prod', os.getenv('PROD_USERNAME'), os.getenv('PASS_PROD')),
    ('uat', os.getenv('UAT_USERNAME'), os.getenv('PASS_UAT')),
])
def test_get_username_and_password(platform_tag, expected_username, expected_password):
    username, password = getUsernameAndPassword(platform_tag)
    assert username == expected_username
    assert password == expected_password
