# Writeup-Miner
This script searches for new feeds on medium.com/rss (for now), and if it finds a new post that is not stored in the database, it will store it in a MongoDB database and notify you via Telegram or Discord. <br />
# Installation and Configuration (python 3)
> Please make sure that MongoDB is installed.
```bash
git clone https://github.com/S7r4n6er/writeup-miner.git
cd writeup-miner
pip install -r requirements.txt
```
## Edit config.yaml file
If you want to use this program without command line arguments, you need to edit the config.yaml file. Once you've made the necessary changes, simply run the program.
```bash
python3 writeup-miner.py
```
## Run with command line arguments.
### Notify via Telegram
```bash
python3 writeup-miner.py -v -t <TelegramBot-TOKEN> -c <Chat-id> -H <MongoDB host> -p <MongoDB port> -d <Database Name>
```
### Notify via Discord
```bash
python3 writeup-miner.py -v -w <Discord Webhook> -H <MongoDB host> -p <MongoDB port> -d <Database Name>
```
### If you need to update Database
```bash
python3 writeup-miner.py -v --update
```