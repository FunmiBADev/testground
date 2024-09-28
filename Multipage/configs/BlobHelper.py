import requests
import time

class BlobStorageHelper:
    CLIENT_ID = "abcde"
    CLIENT_SECRET = "12345"
    TENANT_ID = "dunnmyTenID"
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    STORAGE_ACCOUNT = "DUMMY_STORAGE_ACCOUNT"
    ACCOUNT_URL = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net"

    # Class variables for caching the token
    cached_token = None
    token_timestamp = None
    token_expiry_duration = 24 * 60 * 60  # 24 hours in seconds

    @classmethod
    def getBlobToken(cls):
        """Fetch a new access token and cache it."""
        payload = {
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'grant_type': 'client_credentials',
            'scope': f"https://{cls.STORAGE_ACCOUNT}.blob.core.windows.net/.default"
        }
        
        response = requests.post(cls.TOKEN_URL, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            # Cache the new token and store the current timestamp
            cls.cached_token = access_token
            cls.token_timestamp = time.time()
        else:
            raise Exception(f"Error fetching token: {response.status_code}, {response.text}")

        # Return the cached token
        return "Bearer " + cls.cached_token

    @classmethod
    def refresh_token(cls):
        """Check if the token has expired, and refresh it if necessary."""
        current_time = time.time()

        # If token exists and hasn't expired, return the cached token
        if cls.cached_token and cls.token_timestamp:
            if current_time - cls.token_timestamp < cls.token_expiry_duration:
                return "Bearer " + cls.cached_token
        
        # If token doesn't exist or has expired, get a new one
        return cls.getBlobToken()

# Example usage:
# token = BlobStorageHelper.refresh_token()
# print(token)
