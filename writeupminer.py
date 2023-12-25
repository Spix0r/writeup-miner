from modules.Logger import logger
from modules.scrape import scrape
from modules.Logger import Color
from modules import filedb
from modules import mongodb
import os, pymongo, argparse

HOMEPATH = os.path.expanduser('~')
WORKINGDIR = os.path.dirname(os.path.abspath(__file__))
FILEDBDIR = HOMEPATH + "/.wiretupminer/feeds/feedsDB.txt"

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
    parser.add_argument("-l", "--urls", help="urls.txt list file path" , default=f"{WORKINGDIR}/res/urls.txt")
    parser.add_argument("-t", "--token", help="Telegram Bot token")
    parser.add_argument("-c", "--chatid", help="Telegram chatid")
    parser.add_argument("-m", "--dbmode", help="db mode (file/mongo)", default="file")
    parser.add_argument("-u", "--update", action="store_true", help="Update Database")
    parser.add_argument("-f", "--filter", help="filter some words in feed's title", default=f"{WORKINGDIR}/res/filters.txt")

    return parser.parse_args()

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
            filedb.checkDatabase(newFeeds, FILEDBDIR, args.token, args.chatid, filtered_words)

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
            mongodb.check_database(mydb, newFeeds, args.token, args.chatid, filtered_words)
        else:
            mongodb.updateDatabase(mydb, newFeeds, exist=is_exist)

if __name__ == "__main__":
    main()