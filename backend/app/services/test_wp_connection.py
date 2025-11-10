import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

WP_API_URL = os.getenv("WP_API_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

def test_wp_connection():
    print("Testing connection to WordPress API...")
    try:
        response = requests.get(
            WP_API_URL,
            auth=HTTPBasicAuth(WP_USER, WP_APP_PASSWORD),
            timeout=15
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Successfully connected to WordPress API.")
            print(f"Returned {len(response.json())} items.")
        else:
            print(f"❌ Failed: {response.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_wp_connection()
