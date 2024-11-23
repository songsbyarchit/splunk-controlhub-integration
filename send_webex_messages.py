import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Webex credentials
WEBEX_ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID")

# Webex API URL
WEBEX_API_URL = "https://webexapis.com/v1/messages"

# Messages to send
MESSAGES = [
    "Can we prioritize the client deliverables over the internal review this week?",
    "Quick heads-up: The latest firmware update resolves the VPN connectivity issue.",
    "Just a reminder: Team building event scheduled for next Wednesday at 5 PM.",
    "Can someone confirm if the QA environment is ready for testing the new feature?",
    "Congrats to the team on securing the partnership deal! Well done!",
    "Please don't forget to log your hours in the time tracking system today.",
    "Do we need to book a larger conference room for the upcoming workshop?",
    "Here's the draft proposal for review: Let me know if you'd like any changes.",
    "Is there a standard template for creating customer-facing slide decks?",
    "The security team has flagged the issue. Please ensure compliance by tomorrow.",
    "FYI: The new helpdesk system goes live on Monday. Check your emails for details.",
    "Does anyone have a spare USB-C cable? Mine just stopped working.",
    "Please review the onboarding checklist and let me know if I missed anything.",
    "The IT support line will be temporarily unavailable from 2 PM to 4 PM today.",
    "Amazing work on the beta release! The feedback so far has been fantastic.",
    "Here's the shared drive link for the training materials: [shared link].",
    "Are we good to share the product roadmap with the client next week?",
    "I'm putting together a knowledge base article. Any tips or resources to include?",
    "Can someone clarify the expected downtime for the database migration this weekend?",
    "The new product demo is scheduled for Thursday at 10 AM. Let’s all be prepared!"
]

# Webex headers
headers = {
    "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Send messages to Webex
for message in MESSAGES:
    payload = {
        "roomId": WEBEX_ROOM_ID,
        "text": message
    }
    response = requests.post(WEBEX_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Message sent: {message}")
    else:
        print(f"Failed to send message: {message}")
        print(f"Response: {response.status_code}, {response.text}")