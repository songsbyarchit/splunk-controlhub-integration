import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Webex Access Token from .env
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")

# Ensure the access token exists
if not WEBEX_ACCESS_TOKEN:
    print("Error: Missing WEBEX_ACCESS_TOKEN in .env file.")
    exit(1)

# Define the API endpoint and headers
url = "https://webexapis.com/v1/rooms"
headers = {
    "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Room details
payload = {
    "title": "Splunk Alerts Room"  # Customize your room name
}

# Make the POST request to create a room
response = requests.post(url, headers=headers, json=payload)

# Debugging output
print(f"Response Status Code: {response.status_code}")
print(f"Response Content: {response.text}")

if response.status_code == 200:
    room_data = response.json()
    print("Room created successfully!")
    print(f"Room ID: {room_data['id']}")
else:
    print(f"Error creating room: {response.status_code}, {response.text}")