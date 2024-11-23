import os
import requests
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv()

# Webex credentials
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")

# Splunk HEC credentials
SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")

# Fetch messages from Webex
webex_headers = {
    "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
webex_endpoint = f"https://webexapis.com/v1/messages?roomId={WEBEX_ROOM_ID}&max=100"  # Adjust max number of messages as needed

def calculate_word_frequency(message):
    # Count word frequency
    words = message.lower().split()
    return dict(Counter(words))

try:
    webex_response = requests.get(webex_endpoint, headers=webex_headers)
    if webex_response.status_code == 200:
        messages = webex_response.json().get("items", [])
        print(f"Fetched {len(messages)} messages from Webex.")

        # Process and send word frequency to Splunk
        splunk_headers = {
            "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}"
        }
        for message in messages:
            text = message.get("text", "")
            word_frequency = calculate_word_frequency(text)
            splunk_payload = {
                "event": {"original_message": text, "word_frequency": word_frequency},
                "sourcetype": "webex:message"
            }
            splunk_response = requests.post(
                SPLUNK_HEC_URL,
                headers=splunk_headers,
                json=splunk_payload,
                verify=False
            )
            if splunk_response.status_code != 200:
                print(f"Error sending data to Splunk: {splunk_response.status_code}, {splunk_response.text}")
            else:
                print("Message sent to Splunk successfully!")
    else:
        print(f"Error fetching messages from Webex: {webex_response.status_code}, {webex_response.text}")
except Exception as e:
    print(f"Connection failed: {e}")