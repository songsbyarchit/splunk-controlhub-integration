import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Webex Access Token
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")

# Check if the token exists
if not WEBEX_ACCESS_TOKEN:
    print("Error: Missing Webex Access Token in .env file.")
    exit(1)

# Define the API endpoint
url = "https://webexapis.com/v1/people/me"

# Set up the headers
headers = {
    "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}"
}

# Make the API call
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("API Test Successful! User Details:")
    print(response.json())
else:
    print(f"API Test Failed! Status Code: {response.status_code}")
    print(response.text)