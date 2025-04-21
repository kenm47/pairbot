# Slack Pair Bot

Pairs random users in a Slack channel every two weeks.

## Setup
1. Create a Slack app with required scopes: `channels:read`, `chat:write`, `users:read`, `conversations.members`
2. Install the app and get your Bot Token and Channel ID.
3. Set GitHub secrets:
   - `SLACK_BOT_TOKEN`
   - `SLACK_CHANNEL_ID`
4. Push code to GitHub. It runs automatically every two weeks.

## Local Testing
```bash
export SLACK_BOT_TOKEN=your-token
export SLACK_CHANNEL_ID=your-channel-id
python slack_pair_bot.py
```
