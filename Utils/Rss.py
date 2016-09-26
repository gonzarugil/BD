import feedparser
import operator
import Utils.Time
# Obtenemos las noticias a través del RSS


def getrss(url):
    feed = feedparser.parse(url)
    feed["entries"].sort(key=operator.itemgetter('date'))
    return feed


def getrssdays(feed):
    days = []
    for i in range(0, len(feed['entries'])):
        currentpost = feed['entries'][i]
        postdate = Utils.Time.formatTime((currentpost['date_parsed']))
        if postdate not in days:
            days.append(postdate)
        days.sort()
    return days


# TODO: check if it can be done in other way
def getdayposts(feed, dayformatted):
    posts = []
    numposts = 0
    for i in range(0, len(feed['entries'])):
        currentpost = feed['entries'][i]
        postdate = Utils.Time.formatTime(currentpost['date_parsed'])
        if dayformatted == postdate:
            posts.append({
                'title': currentpost.title,
                'description': currentpost.summary,
                'url': currentpost.link,
            })
            numposts += 1
    return posts
