# Writeup-Miner

**Writeup-Miner** is a flexible tool designed to scrape new Medium RSS feeds, store them in either a MongoDB database or a text file, and send real-time notifications via Telegram or Discord. Whether you're a security researcher or a technology enthusiast, this tool will help you stay updated with the latest content from Medium.

## Features

- Scrape new Medium posts via RSS.
- Store data in MongoDB or a `.txt` file.
- Filter posts based on keywords.
- Real-time notifications via Telegram or Discord.
- Easy setup and use with command-line options.

## Prerequisites

- Python 3.x
- MongoDB (optional, only if you intend to use MongoDB as the database)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xSpidey/writeup-miner.git
   cd writeup-miner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can use Writeup-Miner with either a MongoDB database or a simple `.txt` file for storing the RSS feeds.

### 1. MongoDB Mode

First, ensure MongoDB is installed and running on your system. You can start MongoDB by running:
```bash
sudo service mongod start
```

Then run the script with MongoDB as the storage option:
```bash
python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Telegram Chat ID> -H <MongoDB host> -p <MongoDB port> -m mongo
```

- **Telegram Bot TOKEN**: The token for your Telegram bot.
- **Telegram Chat ID**: The chat ID where notifications will be sent.
- **MongoDB host**: MongoDB host (default: localhost).
- **MongoDB port**: MongoDB port (default: 21017).

#### Updating MongoDB:
```bash
python3 writeup-miner.py -m mongo --update
```

### 2. File Mode

If you prefer not to use MongoDB, you can store the data in a simple `.txt` file:
```bash
python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Telegram Chat ID> -m file
```

#### Updating File Database:
```bash
python3 writeup-miner.py -m file --update
```

### 3. Notify via Telegram

Writeup-Miner supports real-time notifications to a Telegram chat or channel using a bot. To set up notifications via Telegram:

1. Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
2. Obtain the **Bot Token** from BotFather.
3. Get your **Chat ID**:
   - You can use `curl` or any API testing tool to get the chat ID of a group or channel by sending a message and checking the response using Telegram's Bot API.
   - Example of using `curl`:
     ```bash
     curl "https://api.telegram.org/bot<your_bot_token>/getUpdates"
     ```
4. Run the script:
   ```bash
   python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Telegram Chat ID> -m mongo
   ```

**Example with a MongoDB Database:**
```bash
python3 writeup-miner.py -t 123456789:ABCdefGhIJKlmnoPQRstuVWxYZ -c -987654321 -m mongo
```

**Example with a .txt file:**
```bash
python3 writeup-miner.py -t 123456789:ABCdefGhIJKlmnoPQRstuVWxYZ -c -987654321 -m file
```

### 4. Notify via Discord

Writeup-Miner also supports Discord notifications. Use the following command to send alerts via Discord:
```bash
python3 writeup-miner.py -m mongo -w <your_discord_webhook>
```

- **Webhook**: Discord webhook URL for receiving notifications.

## Filter Notifications

You can filter notifications by creating a custom list of keywords. Add each word to a new line in the `res/filters.txt` file. Posts that contain these words will be filtered out from your notifications.

## Help and Parameters

For a full list of available parameters, you can always use the `-h` flag:
```bash
python3 writeup-miner.py -h
```

### Available Parameters

| Flag               | Description                                           | Default Value                                 |
|--------------------|-------------------------------------------------------|-----------------------------------------------|
| `-H`, `--host`      | MongoDB host                                          | localhost                                     |
| `-p`, `--port`      | MongoDB port                                          | 21017                                         |
| `-d`, `--database`  | MongoDB database name                                 | writeupminer                                  |
| `-l`, `--urls`      | Path to the list of RSS URLs to scrape                | `${WORKINGDIR}/res/urls.txt`                  |
| `-m`, `--dbmode`    | Database mode (file or mongo)                         | file                                          |
| `-f`, `--filter`    | Path to the filter file                               | `${WORKINGDIR}/res/filters.txt`               |
| `-u`, `--update`    | Update the database (flag)                            | N/A                                           |
| `-t`, `--token`     | Telegram bot token                                    | N/A                                           |
| `-c`, `--chatid`    | Telegram chat ID                                      | N/A                                           |
| `-w`, `--webhook`   | Discord webhook URL                                   | N/A                                           |
| `-v`, `--version`   | Display version information                           | N/A                                           |

---

Let me know if you need further adjustments!
