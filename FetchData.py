import Utils
import TDM
import Config

feed = Utils.Rss.getrss(Config.RSS_URL)
# Retrieve the days of the news in a list **** This has to be saved along with the titles
dayslist = Utils.Rss.getrssdays(feed)
TDM.writeDaysList(dayslist)
# Getting a list of the titles (this is unused)
titlelist = []
for entry in feed["entries"]:
    titlelist.append(entry["title"])

TDM.writeTitleList(titlelist)
# Retrieve all news from feed and save them to csv
TDM.saveallcsv(feed, dayslist)
