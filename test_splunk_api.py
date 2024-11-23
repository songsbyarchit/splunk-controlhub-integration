import os
import requests
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Splunk credentials
SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME")
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD")

# Check environment variables
if not all([SPLUNK_URL, SPLUNK_USERNAME, SPLUNK_PASSWORD]):
    print("Error: Missing Splunk credentials in .env file.")
    exit(1)

# API endpoint for search jobs
search_endpoint = f"{SPLUNK_URL}/services/search/jobs"
search_query = "search index=_internal | head 5"

# Create the search job payload
data = {
    "search": search_query,
    "output_mode": "json"
}

# Send the search request
try:
    response = requests.post(
        search_endpoint,
        auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD),
        data=data,
        verify=False  # Skip SSL verification for now
    )

    # Print out response details for debugging
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)

    # Handle success
    if response.status_code == 201:
        job_id = response.json()["sid"]
        print(f"Search job created successfully! Job ID: {job_id}")
    else:
        print(f"Error creating search job: {response.status_code}, {response.text}")

except Exception as e:
    print(f"Connection failed: {e}")