# Attendance Telegram Bot

This project implements a Telegram bot used for tracking employee attendance. The bot allows staff to register their account, check in with a live location when work starts, and check out with a location, photo and short description when work finishes. Attendance data is stored in Google Sheets.

## Required environment variables

The bot expects the following variables to be available in the environment:

- `API_TOKEN` – Telegram Bot API token.
- `SHEET_URL_EMPLOYEES` – URL of the Google Sheet that contains employee details.
- `SHEET_URL_ATTENDANCE` – URL of the Google Sheet where attendance records are stored.
- `SHEET_URL_LOCATION` – URL of the Google Sheet that lists office locations.

In addition, Google service account credentials must be provided either via `GOOGLE_CREDS_JSON` (JSON string) or by pointing `CREDS_FILE` to a credentials file. `WORKSHEET_NAME` can be set to choose a different worksheet name for location data (defaults to `offices`).

## Installation

1. Ensure Python 3.10 or newer is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the bot

Set the environment variables listed above and then start the bot:

```bash
python main.py
```

The bot will connect to Telegram and begin handling commands such as `/register`, `/checkin` and `/checkout`.
