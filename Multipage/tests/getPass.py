import os
from dotenv import load_dotenv

def getUsernameAndPassword(platform_tag):
    # Load the environment variables from the .env file
    load_dotenv()

    # Check the value of platform_tag and return the appropriate credentials
    if 'PROD' in platform_tag:
        return os.getenv('PROD_USERNAME'), os.getenv('PASS_PROD')
    else:
        return os.getenv('UAT_USERNAME'), os.getenv('PASS_UAT')

# Example usage:
platform_tag = 'PROD'  # or 'UAT', based on your requirement
username, password = getUsernameAndPassword(platform_tag)
print(f'Username: {username}, Password: {password}')

# Example usage:
platform_tag2 = 'DEMO PLAT 1'  # or 'UAT', based on your requirement
username, password = getUsernameAndPassword(platform_tag2)
print(f'Username: {username}, Password: {password}')

