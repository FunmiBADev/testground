# Your test file, e.g., test_platform_code.py
import os
import pytest
from unittest.mock import patch
from platform_code import get_password

# Fixture to mock environment variables
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('PRODUSERNAME', 'prod_user')
    monkeypatch.setenv('UATUSERNAME', 'uat_user')
    monkeypatch.setenv('PASSPROD', 'prod_pass')
    monkeypatch.setenv('PASSUAT', 'uat_pass')

# Ensure Config class initializes correctly for other tests
@pytest.fixture
def mock_platform_envs():
    global prodUsername, uatUsername, prodPass, uatPass
    prodUsername = os.getenv('PRODUSERNAME')
    uatUsername = os.getenv('UATUSERNAME')
    prodPass = os.getenv('PASSPROD')
    uatPass = os.getenv('PASSUAT')

def test_get_password_uat(mock_env_vars, mock_platform_envs):
    password = get_password("PLATFORM_UAT_1", uatUsername)
    assert password == 'uat_pass'

def test_get_password_prod(mock_env_vars, mock_platform_envs):
    password = get_password("PLATFORM_PROD_1", prodUsername)
    assert password == 'prod_pass'

def test_get_password_empty(mock_env_vars, mock_platform_envs):
    password = get_password("PLATFORM_OTHER", "other_user")
    assert password == ''

if __name__ == '__main__':
    pytest.main()




def test get password_uat(mock_env_vars, mock_platform_envs): 
password = "uatPass"
assert Home_Page.get_password("PLATFORM UAT 1", uatUsername) password 
AssertionError: assert '' == 'uatPass'

- uatPass
streamlit_dashboard\tests\home_page_test.py:89: AssertionError
