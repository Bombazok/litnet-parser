import json
import time
import requests
from datetime import datetime

url = "https://litnet.com/reader/get-page"

# the book title
title = ""

# the first chapter ID (get to the first page of the book and check the last number of the link)
# for example - for 'https://litnet.com/ru/reader/koldovskoi-veresk-b399098?c=4296340' the chapter ID is 4296340
# if it's not presented - use the next comment method to find it, but check the 'Payload' instead of 'Headers'
chapterID = ""

# check 'DevTools Network tab -> get-page request -> Headers -> Request Headers' to put your data here
# do not forget to log in. It won't work if you won't fill this data
csrf = ""
cookie = ""

file = open("books/%s.html" % title, "a")
file.write(
    "<!DOCTYPE html><html><head><meta charset='UTF-8'/><title>%s</title></head><body>" % title)

data = {
    "chapterId": chapterID,
    "page": 1,
}

headers = {
    "x-csrf-token": csrf,
    "cookie": cookie,
}


def getDirtyJSON(data):
    return json.loads(requests.post(url, data, headers=headers).text)


def getJSON(data):
    result = None

    while result is None:
        try:
            time.sleep(1.5)
            result = getDirtyJSON(data)
        except:
            time.sleep(1.5)
            pass

    return result


initialTime = datetime.now()

print("The parsing process has begun. Current time: %s" %
      (initialTime.strftime("%H:%M:%S")))

parsedJSON = getJSON(data)

while True:
    file.write("<h1>%s</h1>" % parsedJSON["chapterTitle"])
    file.write(parsedJSON["data"])

    while parsedJSON["totalPages"] > parsedJSON["page"]:
        data["page"] = parsedJSON["page"] + 1
        parsedJSON = getJSON(data)

        file.write(parsedJSON["data"])

    print("%s has been parsed. Current time: %s" %
          (parsedJSON["chapterTitle"], datetime.now().strftime("%H:%M:%S")))

    if (parsedJSON["nextChapter"]):
        data["chapterId"] = parsedJSON["nextChapter"]["id"]
        data["page"] = 1

        parsedJSON = getJSON(data)
    else:
        file.write("</body></html>")

        print("The book has been successfully parsed. Result time: %s. It took %s seconds" %
              (datetime.now().strftime("%H:%M:%S"), (datetime.now() - initialTime).seconds))

        break
