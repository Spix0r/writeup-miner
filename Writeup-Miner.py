import argparse,pymongo,requests,time,os,sys,urllib.parse,re
import xml.etree.ElementTree as ET
from colorama import Fore
import yaml,ssl

# Logging Function

def logger(silent,message,TYPE):
    if silent == True:
        if TYPE == "error":
            print(Fore.LIGHTCYAN_EX+"["+Fore.LIGHTYELLOW_EX+"✗"+Fore.LIGHTCYAN_EX+"] "+Fore.RED+message+Fore.RESET)
        elif TYPE == "success":
            print(Fore.LIGHTCYAN_EX+"["+Fore.LIGHTYELLOW_EX+"✓"+Fore.LIGHTCYAN_EX+"] "+Fore.LIGHTGREEN_EX+message+Fore.RESET)
        elif TYPE == "pending":
            print(Fore.LIGHTCYAN_EX+"["+Fore.LIGHTYELLOW_EX+"*"+Fore.LIGHTCYAN_EX+"] "+Fore.LIGHTWHITE_EX+message+Fore.RESET)
        time.sleep(0.30)

# load config.yaml

def load_config():
    try:
        __path__ = os.path.dirname(os.path.realpath(__file__))+"/"
        with open(__path__+"config.yaml","r") as f:
            return yaml.load(f.read(),Loader=yaml.FullLoader)
    except Exception as e:
        logger(True,"{}".format(e),"error")
        exit(1)

# Setup argparse


def create_message(args,feed):
    try:
        title = re.sub(r'(?i)(?<!\\)(?:\\\\)*\\u([0-9a-f]{4})', lambda m: chr(int(m.group(1), 16)), feed["title"])
        tags = ""
        if feed["tags"] != []:
            for tag in feed["tags"]:
                if "-" in tag:
                    tag = tag.replace("-","_")
                tags = tags+"#"+tag+" "
        else:
            tags = "No_Tags"
        message = urllib.parse.quote_plus("🔖New Writeup❗️\n———————————————\n🗓Date: {}\n———————————————\n✏️Title: {}\n———————————————\n📎Link: {}\n———————————————\nTags: {}".format(feed["published"],title,feed["url"],tags))
        return message
    
    except Exception as e:
        logger(args.verbose,"{}".format(e),"error")


def setup_argparse():

    parser = argparse.ArgumentParser(description="Writeup Miner")
    parser.add_argument("-v", "--verbose", action="store_true",default=False, help="Show Verbose")
    parser.add_argument("-u", "--update", action="store_true", help="Update Database")
    parser.add_argument("-w", "--webhook", help="Discord Webhook")
    parser.add_argument("-t", "--token" ,help="Telegram Bot token",required='-c' in sys.argv or '--chatid' in sys.argv)
    parser.add_argument("-c", "--chatid",help="Telegram Chat ID",required='-t' in sys.argv or '--token' in sys.argv)
    parser.add_argument("-H", "--host",help="MongoDB host",required='-p' in sys.argv or '--port' in sys.argv)
    parser.add_argument("-p", "--port",help="MongoDB port",required='-H' in sys.argv or '--host' in sys.argv)
    parser.add_argument("-d", "--dbs",help="MongoDB Database name to store feeds on it",required='-p' in sys.argv or '--port' in sys.argv)
    return parser.parse_args()

# Send New Posts to Telegram and Discord

def notify(args,message):
    try:
        if args.webhook:
            logger(args.verbose,"Sending New Posts to Discord","pending")
            #soon
            pass
        elif args.token and args.chatid:
            logger(args.verbose,"Sending New Posts to Telegram","pending")
            chatid = args.chatid
            token = args.token
            message = create_message(args,message)
            req = requests.get(f"https://api.telegram.org/bot{token}/sendmessage?chat_id={chatid}&text={message}")
            logger(args.verbose,"New feed sent successfully","success")
            if req.status_code != 200:
                logger(args.verbose,"Telegram Error : "+req.text,"error")
                exit(1)
    except Exception as e:
        logger(args.verbose,"{}".format(e),"error")
        exit(1)

# Check if Database exists or not

def existdb(args,myclient):
    try:
        logger(args.verbose,"Checking for Database existence.",TYPE="pending")
        dbnames = myclient.list_database_names()
        if "writeupminer" in dbnames:
            logger(args.verbose,"Database Found.",TYPE="success")
            return True
        logger(args.verbose,"Database Not Found.",TYPE="error")
    except Exception as e:
        logger(args.verbose,"{}".format(e),"error")
        exit(1)

def get_urls():
    try:
        urls = []
        __path__ = os.path.dirname(os.path.realpath(__file__))+"/"
        with open(__path__+"res/links.txt",'r') as f:
            lines = [line.rstrip() for line in f]
            for url in lines:
                if "/tag/" not in url:
                    url = url + "feed"
                urls.append(url)
        return urls
    except Exception as e:
        logger(True,"{}".format(e),"error")
        exit(1)    

# get feed

def parsefeeds(url):
    try:
        rss_url = url
        response = requests.get(rss_url)
        time.sleep(5)
        if response.ok:
            root = ET.fromstring(response.content)
            feeds_list = []
            feeds_obj = {}
            for item in root.iter("item"):
                title = item.find("title").text
                guid = item.find("guid").text
                published = item.find("pubDate").text
                tags = item.findall("category")
                tag_list = []
                if tags != []:
                    for tag in tags:
                        tag_list.append(tag.text)
                else:
                    tag_list = []
                feeds_obj = {"title": title, "url": guid, "published": published, "tags": tag_list}
                feeds_list.append(feeds_obj)
            return feeds_list
                
        else:
            logger(True,"Error while fetching feeds response : {}".format(response),"error")
            logger(True,"Url : {}".format(rss_url),"error")
            return []
                

    except Exception as e:

        logger(True,"Error while fetching feeds Url : {}".format(rss_url),"error")



def get_feed():
    try:
        logger(True,"Loading Urls.","pending")
        urls = get_urls()
        logger(True,"Urls loaded Successfully","success")
        objects = []
        logger(True,"Loading New Feeds.","pending")

        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        for url in urls:
            feeds = parsefeeds(url)
            if feeds != [] and feeds != None:
                for feed in feeds:
                    if feed not in objects:
                        objects.append(feed)
        logger(True,"New Feeds loaded Successfully","success")
        return objects

    except Exception as e:
        logger(True,"Error : "+str(e),"error")
        exit(1)



def updateDatabase(args,mydb,new_feeds,exist):
    try:
        logger(args.verbose,"Updating Database.",TYPE="pending")
        mycol = mydb["writeups"]
        if exist:
            logger(args.verbose,"Removing previous collection.",TYPE="pending")
            mycol.drop()
        else:
            logger(args.verbose,"Creating new collection.",TYPE="pending")
        mycol.insert_many(new_feeds)
        logger(args.verbose,"Database Updated.",TYPE="success")
    except Exception as e:
        logger(args.verbose,"{}".format(e),TYPE="error")
        exit(1)

def push_to_database(args,mydb,new_feed):
    try:
        logger(args.verbose,"Pushing new posts to database.",TYPE="pending")
        mycol = mydb["writeups"]
        mycol.insert_one(new_feed)
        logger(args.verbose,"Pushed new posts to database.",TYPE="success")
    except Exception as e:
        logger(args.verbose,"{}".format(e),TYPE="error")
        exit(1)


def check_database(args,mydb,new_feeds):
    try:
        logger(args.verbose,"Checking for new posts.",TYPE="pending")
        mycol = mydb["writeups"]
        old_feeds = mycol.find({})
        urls = []
        for old_feed in old_feeds:
            urls.append(old_feed['url'])

        for new_feed in new_feeds:
            if new_feed["url"] not in urls:
                logger(args.verbose,"New Feed Found : "+new_feed["title"],TYPE="success")
                push_to_database(args,mydb,new_feed)
                notify(args,new_feed)
    except Exception as e:
        logger(args.verbose,"{}".format(e),TYPE="error")
        exit(1)


# Main Function
def main():
    args = setup_argparse()
    if not len(sys.argv) > 1:
        conf = load_config()
        args.verbose = conf["args"]["verbose"]
        args.update = conf["args"]["update"]      
        args.webhook = conf["args"]["discord"]["webhook"]
        args.token = conf["args"]["telegram"]["token"]
        args.chatid = conf["args"]["telegram"]["chatid"]
        args.host = conf["mongodb"]["host"]
        args.port = conf["mongodb"]["port"]
        args.dbs = conf["mongodb"]["name"]

    myclient = pymongo.MongoClient("mongodb://{}:{}/".format(args.host,args.port))
    mydb = myclient[args.dbs]
    is_exist = existdb(args,myclient)


    if args.update:
        new_feeds = get_feed()
        updateDatabase(args,mydb,new_feeds,exist=is_exist)
        exit(0)

    if is_exist:
        new_feeds = get_feed()
        check_database(args,mydb,new_feeds)
    else:
        new_feeds = get_feed()
        updateDatabase(args,mydb,new_feeds,exist=is_exist)


if __name__ == "__main__":
    main()
