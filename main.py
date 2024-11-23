import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
SPLUNK_URL = os.getenv("SPLUNK_URL")

if not WEBEX_ACCESS_TOKEN or not SPLUNK_URL:
    print("Error: Missing environment variables. Check your .env file.")
    exit(1)

print("Environment variables loaded successfully!")

# Test Webex API call
headers = {
    "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}"
}

response = requests.get("https://webexapis.com/v1/people/me", headers=headers)

if response.status_code == 200:
    print("Webex API Response:", response.json())
else:
    print("Error calling Webex API:", response.status_code, response.text)