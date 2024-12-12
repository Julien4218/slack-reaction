import os
import requests
import time

# Get the Slack API token and channel ID from environment variables
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not SLACK_API_TOKEN or not CHANNEL_ID:
    raise Exception("SLACK_API_TOKEN and CHANNEL_ID environment variables are required")

# Step 1: Send a message to the Slack channel
def send_message(text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": CHANNEL_ID,
        "text": text
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200 and response.json()["ok"]:
        channel_id = response.json()["channel"]
        timestamp = response.json()["ts"]
        return channel_id, timestamp
    else:
        raise Exception(f"Failed to send message: {response.json()}")

# Step 2: Capture user reactions using the Reactions API
def capture_reactions(channel_id, timestamp):
    print(f"Getting reactions on channel_id: {channel_id}, timestamp: {timestamp}")
    url = "https://slack.com/api/reactions.get"
    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel_id,
        "timestamp": timestamp
    }

    response = requests.get(url, headers=headers, params=data)
    print(f"Got response: {response.json()}")
    if response.status_code == 200 and response.json()["ok"]:
        return response.json()["message"]["reactions"]
    else:
        raise Exception(f"Failed to get reactions: {response.json()}")

def add_reaction(channel_id, timestamp, reaction):
    # print(f"Adding reaction '{reaction}' to message with channel_id: {channel_id}, timestamp: {timestamp}")
    url = "https://slack.com/api/reactions.add"
    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel_id,
        "timestamp": timestamp,
        "name": reaction
    }

    response = requests.post(url, headers=headers, json=data)
    # print(f"Got response: {response.json()}")
    if response.status_code == 200 and response.json()["ok"]:
        print(f"Reaction '{reaction}' added successfully.")
    else:
        raise Exception(f"Failed to add reaction: {response.json()}")

# Step 3: Main function to send message and wait for reactions
def main():
    channel_id, message_ts = send_message("Should I continue? react with :thumbsup: or :thumbsdown:")
    print(f"Message sent. Timestamp: {message_ts}")

    # add_reaction(channel_id, message_ts, "thumbsup")
    # add_reaction(channel_id, message_ts, "thumbsdown")

    # Wait for a certain period to allow users to react (e.g., 30 seconds)
    print("Waiting for reactions...")
    time.sleep(10)

    reactions = capture_reactions(channel_id, message_ts)
    for reaction in reactions:
        print(f"Reaction: {reaction['name']}, Count: {reaction['count']}")

if __name__ == "__main__":
    main()

