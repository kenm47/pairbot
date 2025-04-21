import os
import random
import sqlite3
import time
import requests

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
DB_FILE = "pairs.db"

headers = {
    "Authorization": f"Bearer {SLACK_TOKEN}",
    "Content-Type": "application/json",
}

def init_db():
    print("[DEBUG] Initializing DB")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pairs (
            user1 TEXT,
            user2 TEXT,
            timestamp INTEGER
        )
    """)
    conn.commit()
    conn.close()

def get_bot_user_id():
    resp = requests.get("https://slack.com/api/auth.test", headers=headers).json()
    return resp.get("user_id")

def get_channel_members():
    print(f"[DEBUG] Fetching members for channel: {CHANNEL_ID}")
    url = f"https://slack.com/api/conversations.members?channel={CHANNEL_ID}"
    resp = requests.get(url, headers=headers).json()
    print("[DEBUG] Slack API members response:", resp)
    return resp.get("members", [])

def get_recent_pairs(weeks=4):
    cutoff = int(time.time()) - weeks * 7 * 24 * 3600
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user1, user2 FROM pairs WHERE timestamp > ?", (cutoff,))
    pairs = c.fetchall()
    conn.close()
    return set(tuple(sorted(p)) for p in pairs)

def save_pairs(pairs):
    print("[DEBUG] Saving pairs:", pairs)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = int(time.time())
    for u1, u2 in pairs:
        c.execute("INSERT INTO pairs (user1, user2, timestamp) VALUES (?, ?, ?)", (u1, u2, now))
    conn.commit()
    conn.close()

def post_pairs_to_slack(pairs):
    print("[DEBUG] Posting pairs to Slack")
    for u1, u2 in pairs:
        text = f"<@{u1}> ⮔ <@{u2}>"
        print(f"[DEBUG] Posting message: {text}")
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json={"channel": CHANNEL_ID, "text": text},
        )
        print("[DEBUG] Slack response:", resp.json())

def generate_pairs(members, recent_pairs):
    random.shuffle(members)
    pairs = []
    while len(members) >= 2:
        u1, u2 = members.pop(), members.pop()
        if tuple(sorted((u1, u2))) not in recent_pairs:
            pairs.append((u1, u2))
    return pairs

def main():
    init_db()
    bot_id = get_bot_user_id()
    members = get_channel_members()
    members = [m for m in members if m != "USLACKBOT" and m != bot_id]
    print("[DEBUG] Members after filtering:", members)
    recent = get_recent_pairs()
    pairs = generate_pairs(members, recent)
    if not pairs:
        print("[DEBUG] No valid pairs found. Skipping post.")
        return
    save_pairs(pairs)
    post_pairs_to_slack(pairs)

if __name__ == "__main__":
    main()
