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

        # Poll the job's status
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
                    break  # Exit loop when the job is done
                else:
                    time.sleep(2)  # Wait before polling again
            else:
                print(f"Error checking job status: {status_response.status_code}, {status_response.text}")
                exit(1)

        # Fetch the results after the job is done
        results_endpoint = f"{SPLUNK_URL}/services/search/jobs/{job_id}/results"
        results_response = requests.get(
            results_endpoint,
            auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD),
            params={"output_mode": "json"},
            verify=False
        )

    # Inside the results block
    if results_response.status_code == 200:
        print("Search Job Results:")
        print(json.dumps(results_response.json(), indent=4))  # Pretty-print the results
    else:
        print(f"Error fetching results: {results_response.status_code}, {results_response.text}")

except Exception as e:
    print(f"Connection failed: {e}")