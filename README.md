# Writeup-Miner
This script searches for new feeds on medium.com/rss (for now), and if it finds a new post that is not stored in the database, it will store it in a MongoDB database or a .txt file and notify you via Telegram. <br />
## Installation and Usage (python 3)
> Please make sure that MongoDB is installed.
```bash
git clone https://github.com/0xSpidey/writeup-miner.git
cd writeup-miner
pip install -r requirements.txt
```
### Use Mongo Database
Note : Make sure MongoDB has been installed.
```bash
python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Teleram Chat id> -H <MongoDB host> -p <MongoDB port> -m mongo
```
#### If you want to update Mongo Database
```bash
python3 writeup-miner.py -m mongo --update
```
### Use txt File as Database
```bash
python3 writeup-miner.py -t <Telegram Bot TOKEN> -c <Teleram Chat id>-c <Chat-id> -m file
```
#### If you want to update File Database
```bash
python3 writeup-miner.py -m file --update
```
## Filter words
If you need to filter some words that you don't want to receive notifications for, just put the words in the res/filters.txt file, one word per line.
