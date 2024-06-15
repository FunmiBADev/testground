import os
from dotenv import load_dotenv
import pytest

# Load the test environment variables from the .env.test file
load_dotenv('.env.test')
from logic import main

# Load the test environment variables from the .env.test file
load_dotenv('.env.test')

def test_get_username_and_password_prod():
    platform_tag = 'PROD'
    expected_username = 'demo_your_prod_username'
    expected_password = 'demo_your_prod_password'

    username, password = main.getUsernameAndPassword(platform_tag)
    assert username == expected_username
    assert password == expected_password

def test_get_username_and_password_uat():
    platform_tag = 'UAT'
    expected_username = 'demo_your_uat_username'
    expected_password = 'demo_your_uat_password'

    username, password = main.getUsernameAndPassword(platform_tag)
    assert username == expected_username
    assert password == expected_password

# Additional tests to cover edge cases
def test_get_username_and_password_mixed_case_prod():
    platform_tag = 'prod'
    expected_username = 'demo_your_prod_username'
    expected_password = 'demo_your_prod_password'

    username, password = main.getUsernameAndPassword(platform_tag.upper())
    assert username == expected_username
    assert password == expected_password

def test_get_username_and_password_mixed_case_uat():
    platform_tag = 'uat'
    expected_username = 'demo_your_uat_username'
    expected_password = 'demo_your_uat_password'

    username, password = main.getUsernameAndPassword(platform_tag.upper())
    assert username == expected_username
    assert password == expected_password

if __name__ == "__main__":
    pytest.main()
