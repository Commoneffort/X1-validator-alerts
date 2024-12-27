# Solana Validator Monitoring Script

This script monitors the performance of a Solana validator, focusing on disk usage and skipped block production. It sends alerts to a Telegram chat when thresholds are exceeded.

## Features
- **Disk Usage Monitoring:** Alerts when disk usage exceeds a specified threshold.
- **Skipped Block Alerts:** Notifies when skipped slots exceed the defined threshold.
- **Telegram Notifications:** Sends real-time alerts to your Telegram bot.

## Setup Instructions

### 1. Create a Telegram Bot
1. Open Telegram and search for **BotFather**.
2. Use the `/newbot` command to create a new bot.
3. Follow the prompts and note down the **API token** provided by BotFather.

### 2. Get Your Chat ID
1. Start a chat with your bot by searching for it on Telegram and clicking **Start**.
2. Open this URL in your browser, replacing `<YOUR_BOT_TOKEN>` with your bot's token:
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
3. Look for `"chat":{"id":<CHAT_ID>` in the JSON response. The `<CHAT_ID>` is your chat ID.

### 3. Configure the Script
Edit the script to include the following:
- **`TELEGRAM_BOT_TOKEN`:** Replace `your_bot_token_here` with your bot's API token.
- **`TELEGRAM_CHAT_ID`:** Replace `your_chat_id_here` with your chat ID.
- **`VALIDATOR_IDENTITY`:** Replace `your_validator_identity_pubkey_here` with your validator's public key.
- **`SOLANA_CLI_PATH`:** Adjust the path to your Solana CLI binary if necessary.

### 4. Run the Script
Start the script using:

```bash
python3 your_script.py
