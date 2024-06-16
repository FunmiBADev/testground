import os
import pytest
from unittest.mock import patch

from logic.main import getUsernameAndPassword  # Correct import statement

# Example environment variables to be used in the tests
PROD_USERNAME = 'demo_your_prod_username'
PASS_PROD = 'demo_your_prod_password'
UAT_USERNAME = 'demo_your_uat_username'
PASS_UAT = 'demo_your_uat_password'

@pytest.fixture(scope='module', autouse=True)
def set_env_vars():
    # Patch the environment variables for the duration of the tests
    with patch.dict(os.environ, {
        'PROD_USERNAME': PROD_USERNAME,
        'PASS_PROD': PASS_PROD,
        'UAT_USERNAME': UAT_USERNAME,
        'PASS_UAT': PASS_UAT
    }):
        yield

@pytest.mark.parametrize("platform_tag, expected_username, expected_password", [
    ('PROD', PROD_USERNAME, PASS_PROD),
    ('UAT', UAT_USERNAME, PASS_UAT),
    ('prod', PROD_USERNAME, PASS_PROD),
    ('uat', UAT_USERNAME, PASS_UAT),
])
def test_get_username_and_password(platform_tag, expected_username, expected_password):
    username, password = getUsernameAndPassword(platform_tag)
    assert username == expected_username
    assert password == expected_password

if __name__ == "__main__":
    pytest.main()
