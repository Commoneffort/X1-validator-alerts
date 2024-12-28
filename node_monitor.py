import psutil
import json
import time
from datetime import datetime
import requests
import subprocess

# Telegram bot credentials
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"

# Thresholds for alerts
DISK_USAGE_THRESHOLD = 80  # Trigger alert if disk usage exceeds 80%

# Block skip monitoring
SKIPPED_SLOTS_ALERT_THRESHOLD = 1  # Trigger alert if any block is skipped

# Path to Solana CLI binary
SOLANA_CLI_PATH = "/usr/local/bin/solana"  # Adjust this if your path differs

# Validator identity pubkey
VALIDATOR_IDENTITY = "your_validator_identity_pubkey_here"  # Replace with your validator's identity pubkey


def collect_performance_metrics():
    """
    Collect system metrics like disk usage.
    """
    disk_usage = psutil.disk_usage('/').percent
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    performance_data = {
        "timestamp": current_time,
        "disk_usage": disk_usage,
    }
    return performance_data


def get_skipped_slots():
    """
    Check the skipped slots for the validator using the Solana CLI.
    """
    try:
        # Fetch the validator's block production information
        cmd = [SOLANA_CLI_PATH, "block-production", "--output", "json"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Parse the output as JSON
        data = json.loads(result.stdout)
        for validator in data.get("leaders", []):
            if validator["identityPubkey"] == VALIDATOR_IDENTITY:
                skipped_slots = validator["skippedSlots"]
                return skipped_slots

    except Exception as e:
        print(f"Error fetching skipped slots: {e}")
        return None


def send_telegram_message(message):
    """
    Send a message to Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")


def check_thresholds_and_alert(metrics, skipped_slots):
    """
    Check for threshold violations and send alerts.
    """
    alerts = []

    # Disk usage alert
    if metrics["disk_usage"] > DISK_USAGE_THRESHOLD:
        alerts.append(f"🚨 <b>Disk Usage Alert:</b> {metrics['disk_usage']}% (Threshold: {DISK_USAGE_THRESHOLD}%)")

    # Block skipping alert
    if skipped_slots and skipped_slots >= SKIPPED_SLOTS_ALERT_THRESHOLD:
        alerts.append(f"🚨 <b>Block Skipping Alert:</b> {skipped_slots} slots skipped!")

    if alerts:
        message = "\n".join(alerts)
        send_telegram_message(message)


def save_performance_data(data):
    """
    Save performance data to a JSON file.
    """
    with open("performance_data.json", "a") as f:
        f.write(json.dumps(data) + "\n")


def main():
    """
    Main function to monitor performance metrics and skipped slots.
    """
    last_skipped_slots = 0  # Keep track of the last skipped slots count

    while True:
        # Collect system metrics
        metrics = collect_performance_metrics()

        # Check for skipped slots
        skipped_slots = get_skipped_slots()

        # Check for new skips and trigger alerts
        if skipped_slots is not None and skipped_slots > last_skipped_slots:
            new_skips = skipped_slots - last_skipped_slots
            last_skipped_slots = skipped_slots  # Update last skipped slots count
            metrics["skipped_slots"] = skipped_slots
            check_thresholds_and_alert(metrics, new_skips)

        # Save performance metrics
        save_performance_data(metrics)
        print(metrics)  # Print the metrics for immediate feedback

        time.sleep(60)  # Monitor every minute


if __name__ == "__main__":
    main()
