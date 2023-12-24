from .Logger import logger
import requests, re, urllib

def create_message(feed):
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
        logger("{}".format(e),"ERR")

def notify(token, chatid, message):
    try:
        logger("Sending New Posts to Telegram","INF")
        message = create_message(message)
        req = requests.get(f"https://api.telegram.org/bot{token}/sendmessage?chat_id={chatid}&text={message}")
        logger("New feed sent successfully","OK")
        if req.status_code != 200:
            logger("Telegram Error : "+req.text,"ERR")
            exit(1)
    except Exception as e:
        logger("{}".format(e),"ERR")
        exit(1)