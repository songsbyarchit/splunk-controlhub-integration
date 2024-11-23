import os
import requests
from dotenv import load_dotenv
import urllib3
import time
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Splunk credentials
SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME")
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD")

# Webex credentials
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")

# Check environment variables
if not all([SPLUNK_URL, SPLUNK_USERNAME, SPLUNK_PASSWORD, WEBEX_ACCESS_TOKEN, WEBEX_ROOM_ID]):
    print("Error: Missing credentials in .env file.")
    exit(1)

# Splunk API endpoint for search jobs
search_endpoint = f"{SPLUNK_URL}/services/search/jobs"
search_query = "search index=_internal | head 5"

# Create the search job payload
data = {
    "search": search_query,
    "output_mode": "json"
}

try:
    # Step 1: Create the search job
    response = requests.post(
        search_endpoint,
        auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD),
        data=data,
        verify=False
    )
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)

    if response.status_code == 201:
        job_id = response.json()["sid"]
        print(f"Search job created successfully! Job ID: {job_id}")

        # Step 2: Poll the job's status
        status_endpoint = f"{SPLUNK_URL}/services/search/jobs/{job_id}"
        while True:
            status_response = requests.get(
                status_endpoint,
                auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD),
                params={"output_mode": "json"},
                verify=False
            )

            if status_response.status_code == 200:
                job_status = status_response.json().get("entry", [])[0].get("content", {}).get("dispatchState")
                print(f"Job Status: {job_status}")
                if job_status == "DONE":
                    break
                else:
                    time.sleep(2)
            else:
                print(f"Error checking job status: {status_response.status_code}, {status_response.text}")
                exit(1)

        # Step 3: Fetch the search results
        results_endpoint = f"{SPLUNK_URL}/services/search/jobs/{job_id}/results"
        results_response = requests.get(
            results_endpoint,
            auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD),
            params={"output_mode": "json"},
            verify=False
        )

        if results_response.status_code == 200:
            results = results_response.json().get("results", [])
            if not results:
                print("No results found.")
                exit(0)

            # Extract key fields (e.g., _time and _raw)
            message = "Splunk Search Results:\n"
            for result in results[:5]:  # Limit to the first 5 results
                message += f"Time: {result['_time']}, Event: {result['_raw']}\n"

            # Step 4: Send the results to Webex
            webex_endpoint = "https://webexapis.com/v1/messages"
            webex_headers = {
                "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            webex_payload = {
                "roomId": WEBEX_ROOM_ID,
                "text": message
            }
            webex_response = requests.post(
                webex_endpoint,
                headers=webex_headers,
                json=webex_payload
            )

            if webex_response.status_code == 200:
                print("Message sent to Webex successfully!")
            else:
                print(f"Error sending message to Webex: {webex_response.status_code}, {webex_response.text}")
        else:
            print(f"Error fetching results: {results_response.status_code}, {results_response.text}")
    else:
        print(f"Error creating search job: {response.status_code}, {response.text}")

except Exception as e:
    print(f"Connection failed: {e}")