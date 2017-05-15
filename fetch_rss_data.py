import Utils
import term_document_matrix
import config_vars

feed = Utils.Rss.getrss(config_vars.RSS_URL)
# Retrieve the days of the news in a list **** This has to be saved along with the titles
dayslist = Utils.Rss.getrssdays(feed)
term_document_matrix.writeDaysList(dayslist)
# Getting a list of the titles (this is unused)
titlelist = []
for entry in feed["entries"]:
    titlelist.append(entry["title"])

term_document_matrix.writeTitleList(titlelist)
# Retrieve all news from feed and save them to csv
term_document_matrix.saveallcsv(feed, dayslist)
