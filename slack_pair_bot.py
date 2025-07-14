import os
import random
import requests
import datetime

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

headers = {
    "Authorization": f"Bearer {SLACK_TOKEN}",
    "Content-Type": "application/json",
}

def get_bot_user_id():
    resp = requests.get("https://slack.com/api/auth.test", headers=headers).json()
    return resp.get("user_id")

def get_channel_members():
    print(f"[DEBUG] Fetching members for channel: {CHANNEL_ID}")
    url = f"https://slack.com/api/conversations.members?channel={CHANNEL_ID}"
    resp = requests.get(url, headers=headers).json()
    print("[DEBUG] Slack API members response:", resp)
    return resp.get("members", [])

def post_pairs_to_slack(pairs):
    print("[DEBUG] Posting pairs to Slack")
    for group in pairs:
        if len(group) == 2:
            u1, u2 = group
            text = f"<@{u1}> meet with <@{u2}>"
        elif len(group) == 3:
            u1, u2, u3 = group
            text = f"<@{u1}>, <@{u2}>, and <@{u3}> meet together"
        else:
            continue  # Skip invalid groups
        
        print(f"[DEBUG] Posting message: {text}")
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json={"channel": CHANNEL_ID, "text": text},
        )
        print("[DEBUG] Slack response:", resp.json())

def generate_pairs(members):
    random.shuffle(members)
    pairs = []
    
    # If odd number of members, create one group of three
    if len(members) % 2 == 1 and len(members) >= 3:
        u1, u2, u3 = members.pop(), members.pop(), members.pop()
        pairs.append((u1, u2, u3))
    
    # Pair the remaining members
    while len(members) >= 2:
        u1, u2 = members.pop(), members.pop()
        pairs.append((u1, u2))
    
    return pairs

def main():
    # Check if current ISO week is odd - exit early for true bi-weekly behavior
    current_iso_week = datetime.date.today().isocalendar()[1]
    if current_iso_week % 2 == 1:
        print(f"[DEBUG] Current ISO week {current_iso_week} is odd. Skipping execution for bi-weekly schedule.")
        return
    
    print(f"[DEBUG] Current ISO week {current_iso_week} is even. Proceeding with pair generation.")
    bot_id = get_bot_user_id()
    members = get_channel_members()
    members = [m for m in members if m != "USLACKBOT" and m != bot_id]
    print("[DEBUG] Members after filtering:", members)
    pairs = generate_pairs(members)
    if not pairs:
        print("[DEBUG] No valid pairs found. Skipping post.")
        return
    post_pairs_to_slack(pairs)

if __name__ == "__main__":
    main()
