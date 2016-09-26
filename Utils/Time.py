import time


# Format and unformat work both in single times and in lists
def unformatTime(timeform):
    return time.strp(timeform, "%Y - %m - %d")


def formatTime(datein):
    return time.strftime("%Y - %m - %d", datein)


def todayformatted():
    today = time.time()
    todaystr = formatTime(today)
    print("Today its " + todaystr)
    return todaystr
