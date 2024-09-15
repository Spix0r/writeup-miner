from modules.Logger import logger
from modules.scrape import scrape
from modules.Logger import Color
from modules import filedb
from modules import mongodb
import os, pymongo, argparse

HOMEPATH = os.path.expanduser('~')
WORKINGDIR = os.path.dirname(os.path.abspath(__file__))
FILEDBDIR = HOMEPATH + "/.wiretupminer/feeds/feedsDB.txt"
VERSION=2.0

def displayBanner():
    print(Color.YELLOW+
    r"""
  _      __    _ __                  __  ____             
 | | /| / /___(_) /____ __ _____    /  |/  (_)__  ___ ____
 | |/ |/ / __/ / __/ -_) // / _ \  / /|_/ / / _ \/ -_) __/
 |__/|__/_/ /_/\__/\__/\_,_/ .__/ /_/  /_/_/_//_/\__/_/   
                          /_/                             
    """+Color.RESET)
    

def setup_argparse():
    """
    Parse Command line arguments
    """
    parser = argparse.ArgumentParser(description="Writeup Miner")
    parser.add_argument("-H", "--host", help="MongoDB host", default="localhost")
    parser.add_argument("-p", "--port", help="MongoDB port", default="21017")
    parser.add_argument("-d", "--database", help="MongoDB Database name to store feeds on it", default="writeupminer")
    parser.add_argument("-l", "--urls", help="urls.txt list file path", default=f"{WORKINGDIR}/res/urls.txt")
    parser.add_argument("-m", "--dbmode", help="db mode (file/mongo)", default="file")
    parser.add_argument("-f", "--filter", help="A .txt file containing filter words is used to filter specific words from the feed's title.", default=f"{WORKINGDIR}/res/filters.txt")
    parser.add_argument("-u", "--update", action="store_true", help="Update Database")
    parser.add_argument("-t", "--token", help="Telegram Bot token")
    parser.add_argument("-c", "--chatid", help="Telegram chatid")
    parser.add_argument("-w", "--webhook", help="Discord webhook")
    parser.add_argument("-v", "--version", help="Display version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print("Version : {}".format(VERSION))
        exit(0)

    if args.update:
        return args

    if args.webhook:
        return args

    if not (args.token and args.chatid):
        parser.error("Both -t/--token and -c/--chatid are required unless using -u/--update or -w/--webhook.")

    return args

def main():
    displayBanner()
    args = setup_argparse()
    logger("loading {} file ...".format(args.urls), "INF")
    urls = filedb.loadDatabase(args.urls)
    if urls == []:
        logger("No urls found!", "ERR")
        exit(1)
    logger("loading filters file : {} ..".format(args.filter), "INF")
    filtered_words = filedb.loadDatabase(args.filter)
    newFeeds = scrape(urls)

    if args.dbmode == "file":
        
        logger("Checking DB Directory ...", "INF")
        filedb.makeDatabaseDir(os.path.join(HOMEPATH + '/.wiretupminer/feeds'))

        if args.update:
            logger("Updating FileDB ...", "INF")
            updateFeeds = []
            for feed in newFeeds:
                updateFeeds.append(feed["url"].strip())
            filedb.pushDatabase(updateFeeds, FILEDBDIR)
            logger("FileDB Updated!", "OK")
            exit(0)

        if os.path.exists(FILEDBDIR):
            filedb.checkDatabase(newFeeds, FILEDBDIR, args.webhook, args.token, args.chatid, filtered_words)

        else:
            firstFeeds = []
            logger("feeds.txt not found, Updating Database for first time.", "INF")
            for feed in newFeeds:
                firstFeeds.append(feed["url"].strip())
            filedb.pushDatabase(firstFeeds, FILEDBDIR)

    elif args.dbmode == "mongo":
        myclient = pymongo.MongoClient("mongodb://{}:{}/".format(args.host, args.port))
        mydb = myclient[args.database]
        is_exist = mongodb.existdb(myclient)

        if args.update:
            logger("Updating MongoDB ...", "INF")
            mongodb.updateDatabase(mydb, newFeeds, exist=is_exist)
            logger("MongoDB Updated!", "OK")
            exit(0)

        if is_exist:
            mongodb.check_database(mydb, newFeeds, args.webhook, args.token, args.chatid, filtered_words)
        else:
            mongodb.updateDatabase(mydb, newFeeds, exist=is_exist)

if __name__ == "__main__":
    main()
