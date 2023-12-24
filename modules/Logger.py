from datetime import datetime

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    DARK_GREEN = '\033[32m'
    RESET = '\033[0m'

def logger(log, log_type=None):

    color_map = {
        "ERR": Color.RED,
        "OK": Color.DARK_GREEN,
        "INF": Color.DARK_GRAY
    }
    if log_type in color_map:
        color = color_map[log_type]
        formatted_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        if log_type == "OK":

            print(f"{color}[{log_type}  {formatted_time}] {Color.RESET}{log}{Color.RESET}")
        else:
            print(f"{color}[{log_type} {formatted_time}] {log}{Color.RESET}")

    else:
        print(log)