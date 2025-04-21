import os
import random
import sqlite3
import time
import requests

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # You set this in GitHub Actions secrets
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")  # Same here
DB_FILE = "pairs.db"

# Slack API headers
headers = {
    "Authorization": f"Bearer {SLACK_TOKEN}",
    "Content-Type": "application/json",
}

def init_db():
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

def get_channel_members():
    url = f"https://slack.com/api/conversations.members?channel={CHANNEL_ID}"
    resp = requests.get(url, headers=headers).json()
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
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = int(time.time())
    for u1, u2 in pairs:
        c.execute("INSERT INTO pairs (user1, user2, timestamp) VALUES (?, ?, ?)", (u1, u2, now))
    conn.commit()
    conn.close()

def post_pairs_to_slack(pairs):
    for u1, u2 in pairs:
        text = f"<@{u1}> ⮔ <@{u2}>"
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json={"channel": CHANNEL_ID, "text": text},
        )

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
    members = get_channel_members()
    members = [m for m in members if m != "USLACKBOT"]
    recent = get_recent_pairs()
    pairs = generate_pairs(members, recent)
    save_pairs(pairs)
    post_pairs_to_slack(pairs)

if __name__ == "__main__":
    main()