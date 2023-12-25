# Writeup-Miner

Writeup-Miner is a versatile script designed to scour medium.com/rss for new feeds. When it discovers a fresh post not stored in the database, it saves it to either a MongoDB database or a .txt file. Additionally, it offers notification alerts via Telegram or Discord.

## Installation and Usage (Python 3)

Ensure that MongoDB is installed before proceeding.

### Installation

```bash
git clone https://github.com/0xSpidey/writeup-miner.git
cd writeup-miner
pip install -r requirements.txt
```

### Using MongoDB

Make sure MongoDB is installed and running.

```bash
python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Telegram Chat id> -H <MongoDB host> -p <MongoDB port> -m mongo
```

To update the MongoDB Database:

```bash
python3 writeup-miner.py -m mongo --update
```

### Using a .txt File as Database

```bash
python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Telegram Chat id> -m file
```

To update the File Database:

```bash
python3 writeup-miner.py -m file --update
```

## Filter Words

Customize the words you want to filter from notifications by adding them to the `res/filters.txt` file, one word per line.

## Notify via Discord
```bash
python3 writeup-miner.py -m mongo -w <your_discord_webhook>
```
## Program Help

For assistance with program parameters:

```bash
python3 writeup-miner.py -h
```

## Parameters

- `-H`, `--host`: MongoDB host (default: "localhost")
- `-p`, `--port`: MongoDB port (default: "21017")
- `-d`, `--database`: MongoDB Database name to store feeds (default: "writeupminer")
- `-l`, `--urls`: File path for the list of URLs (default: `${WORKINGDIR}/res/urls.txt`)
- `-m`, `--dbmode`: Database mode (file/mongo) (default: "file")
- `-f`, `--filter`: File path for feed title filters (default: `${WORKINGDIR}/res/filters.txt`)
- `-u`, `--update`: Update the Database (flag)
- `-t`, `--token`: Telegram Bot token
- `-c`, `--chatid`: Telegram chat ID
- `-w`, `--webhook`: Discord webhook
- `-v`, `--version`: Display version information (flag)
