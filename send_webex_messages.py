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
    "Can we pls prioritize the client deliverables over internal revw this week?",
    "qwick heads-up: The lates firmware update resolves the VPN cnnectivity issue.",
    "Just a rmindr: Team building event schedueld for nxt wednesday at 5pm.",
    "Can smone confirm if the QA envioronment is ready for testing the new featuer?",
    "Congrts to the teem on securing the prtnrship deal! Well done!!!",
    "Pls dont forget to log ur hrs in the time trackng system today.",
    "Do we need to book a large confernce room for the upcoming wrokshop?",
    "Here's the draft proposal for reviw: Let me know if you'd like any chnges.",
    "Is there a standard tmplate for creating customer-facing slied decks?",
    "The security tem has flaged the issue. Please ensur compliance by tmrow.",
    "FYI: The new helpdesk system goes live on Monday. Chek your e-mails for ddetails.",
    "Does any1 have a spare USB-C cable? Mine jusst stopd workin.",
    "Plese review the onboarding checklist and let me kno if I missd anything.",
    "The IT support line will be temporariliy unavailable from 2 PM to 4 PM to day.",
    "Thank you for your hard work on this release. I know it has been a tough couple of weeks, but we’re almost there. Please review the final documents and let me know if anything needs to be changed before the presentation. It's crucial that we get everything right, as this will be presented to the entire team at our upcoming quarterly meeting. I want to make sure we’re all aligned and prepared. Afterward, we’ll need to start preparing for the next phase of the project which will involve more testing and optimization to improve the user experience. Thanks again for your efforts!",
    "Hey, quick reminder, can you please send the finalized sales report for last quarter? I need to share it with the leadership team by end of day.",
    "Got it, I'll circle back to you once I have the update from IT about the server issue, should be available later this afternoon. Thanks!",
    "Just checking if you're free this afternoon to discuss the new client proposal? I want to get your input before we finalize it.",
    "Our weekly all-hands meeting is scheduled for 4 PM today, please make sure you’ve reviewed the agenda beforehand so we can dive right into the updates.",
    "FYI: The network maintenance has been postponed until next Friday. No impact on current projects, just a heads-up for the internal systems team.",
    "Can someone send me the link to the latest project plan? I can’t find it in the drive and need it for the upcoming client call.",
    "Do we have any updates from the vendor regarding the shipment of hardware? We’re waiting on that before we can finalize the installation schedule for the new servers.",
    "Looking forward to seeing everyone at the team building event tomorrow. We’ve got a jam-packed agenda, and it’s going to be a lot of fun. Don't forget to bring your energy and enthusiasm, we’ll start right at 9 AM with an icebreaker activity. After that, we’ll split into smaller groups for team challenges, followed by a working lunch. The day will wrap up with a closing discussion on how we can implement what we learned into our daily workflows. It’s going to be a great day, and I can’t wait to see everyone there!",
    "Just wanted to check in with you to see if you had any questions about the new project timelines. We need to ensure that all tasks are aligned with the overall schedule and that everyone is on track to meet their deadlines. Please review the timeline and let me know if you foresee any delays or issues.",
    "Can we confirm the speaker lineup for next week's conference? I need to finalize the agenda for the event and get everything printed before Monday.",
    "Hey, I’ll be out of the office on Friday for the annual company retreat, but I’ll be back on Monday and will have time to catch up on emails. If there’s anything urgent, feel free to send me a message, and I’ll check it periodically. Otherwise, I look forward to reconnecting with everyone on Monday and getting back into the swing of things!",
    "Just a heads-up, we need to complete the final round of user acceptance testing before next Tuesday. The testing should be done by then to avoid any delays in the launch schedule. Please coordinate with the testing team to ensure everything is ready.",
    "Can anyone send me the link to the marketing team’s presentation deck for the client pitch? I believe we need to update some parts before the next meeting.",
    "Reminder: Don't forget to submit your performance reviews before the end of the day tomorrow. If you need assistance, let me know.",
    "Is the team ready for the quarterly demo presentation on Friday? Let’s ensure all demos are polished and rehearsed so we can deliver the best experience to the client.",
    "Can we ensure that all documentation is updated before next week’s compliance audit? Please check the shared drive for any gaps and let me know if anything is missing.",
    "I'm working on a presentation for the upcoming team meeting, and I need your feedback on a few slides. Can you please take a look and share any suggestions before the end of today?",
    "Thanks for your patience. The IT team has resolved the server issue, and everything is back online. Please restart your systems to ensure everything functions correctly.",
    "I’m still waiting for the updated spreadsheet from the finance team. We need it to finalize the budget review before the board meeting on Wednesday. Please follow up with them and let me know if there’s any delay.",
    "Just a quick note to remind you to review the attached report before tomorrow’s meeting. I’ve incorporated all the changes we discussed, and everything should be set for approval.",
    "I’m following up on the project plan for the upcoming marketing campaign. Has everyone reviewed the draft and signed off on their respective tasks? Please make sure all your assignments are updated by tomorrow morning so we can begin execution.",
    "Does anyone have the documentation for the new CRM system? I need it for my meeting with the sales team this afternoon to go over some integration details.",
    "Can you share the link to the training materials for the new product launch? I need it to prepare for the internal session next week.",
    "Let’s wrap up the presentation for the client meeting tomorrow. Please finalize the slides and send them to me by the end of the day so I can review them before we meet.",
    "Has anyone spoken to the vendor about the delay in delivery? We need to get an updated timeline for when the hardware will arrive so we can adjust the project schedule accordingly.",
    "Hey, does anyone have feedback on the new version of the app? We need to prioritize fixes before the next release cycle starts, so please share any bugs or improvements you’ve identified."
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