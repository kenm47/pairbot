# Slack Pair Bot

Pairs random users in a Slack channel every two weeks.

You've provided a Python script designed to randomly pair members in a Slack channel and announce these pairs, while also keeping track of recent pairings to avoid repetition. This is a great tool for fostering team connections\!

Here's a **markdown version** of the `README.md` file for your code:

-----

# Slack Pair Bot

This Python script is a simple bot that facilitates team bonding by randomly pairing members within a specified Slack channel. It ensures that recent pairings aren't immediately repeated, encouraging broader interaction among team members.

-----

## Features

  * **Random Pair Generation**: Shuffles and pairs available Slack channel members.
  * **Pairing History**: Uses a SQLite database to remember past pairings and avoids repeating them within a configurable timeframe (default: 4 weeks).
  * **Slack Integration**: Posts the newly generated pairs directly into your designated Slack channel.
  * **Bot Exclusion**: Automatically excludes the bot's own user ID and the generic Slackbot from pairing.

-----

## Getting Started

Follow these steps to set up and run the Slack Pair Bot.

### Prerequisites

Before you begin, ensure you have the following:

  * **Python 3.x** installed.
  * A **Slack Workspace** where you can create a bot.
  * **Admin access** to your Slack workspace to create a Slack App and get API tokens.

### Installation

1.  **Clone this repository** (or copy the script) to your local machine:

    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Install the required Python libraries**:

    ```bash
    pip install requests
    ```

### Slack App Setup

1.  **Create a new Slack App**:

      * Go to the [Slack API website](https://api.slack.com/apps) and click "Create New App".
      * Choose "From scratch" and give your app a name (e.g., "Team Pair Bot") and select your development Slack workspace.

2.  **Add Bot Token Scopes**:

      * Navigate to "OAuth & Permissions" in your app's settings.
      * Under "Bot Token Scopes", add the following permissions:
          * `channels:read` (to get channel members)
          * `chat:write` (to post messages in channels)

3.  **Install the App to Your Workspace**:

      * After adding the scopes, go to "Install App to Workspace" under "OAuth & Permissions" and click "Install to Workspace".
      * Authorize the app. You will receive a **Bot User OAuth Token** (starts with `xoxb-`). Save this token; you'll need it for `SLACK_BOT_TOKEN`.

4.  **Invite the Bot to Your Channel**:

      * In your desired Slack channel, type `/invite @YourBotName` (replace `YourBotName` with the name of your Slack App) to add the bot to the channel.

### Configuration

The bot requires two **environment variables** to run:

  * `SLACK_BOT_TOKEN`: Your Bot User OAuth Token obtained from the Slack App setup (starts with `xoxb-`).
  * `SLACK_CHANNEL_ID`: The ID of the Slack channel where you want the bot to post messages. You can find the channel ID by opening Slack in your browser, navigating to the channel, and looking at the URL (it's the string starting with `C` after `/archives/` or `/messages/`).

You can set these environment variables in your terminal before running the script:

```bash
export SLACK_BOT_TOKEN="xoxb-YOUR_SLACK_BOT_TOKEN"
export SLACK_CHANNEL_ID="YOUR_SLACK_CHANNEL_ID"
```

For persistent configuration, especially in production environments, consider using a `.env` file and a library like `python-dotenv`, or a system-level environment variable manager.

-----

## Usage

Once configured, simply run the Python script:

```bash
python your_script_name.py
```

The script will:

1.  Initialize a SQLite database (`pairs.db`) if it doesn't exist.
2.  Fetch all members from the specified `SLACK_CHANNEL_ID`.
3.  Filter out the bot itself and the `USLACKBOT`.
4.  Generate new pairs, avoiding those made in the last 4 weeks (by default).
5.  Save the new pairs to the database.
6.  Post each generated pair to the Slack channel.

### Running Automatically (e.g., with Cron)

You can schedule this script to run periodically (e.g., weekly) using tools like `cron` on Linux/macOS or Task Scheduler on Windows.

**Example Cron Job (weekly on Monday at 9 AM):**

```cron
0 9 * * 1 /usr/bin/python3 /path/to/your/script/your_script_name.py
```

Make sure the full path to your Python executable and script is correct. Also, ensure that the environment variables (`SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`) are set in the cron environment or hardcoded within the script (though environment variables are preferred for security).

-----

## Database

The script uses a **SQLite database** named `pairs.db` to store past pairings. This allows the bot to remember who has been paired with whom and avoid immediate repetitions.

  * **File**: `pairs.db`
  * **Table**: `pairs`
  * **Columns**:
      * `user1` (TEXT): ID of the first user in a pair.
      * `user2` (TEXT): ID of the second user in a pair.
      * `timestamp` (INTEGER): Unix timestamp when the pair was created.

-----

## Customization

  * **Recent Pairs Window**: By default, the bot remembers pairs for the last 4 weeks. You can adjust this by modifying the `weeks` parameter in the `get_recent_pairs` function call within `main()`.

-----

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

-----

## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

-----
