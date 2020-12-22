import requests
from bs4 import BeautifulSoup
import json
import re


def clean_string(input):
    return re.sub("[^0-9a-zA-Z]", "", input).lower()

URLS = [
    f"https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_{year}" for year in range(1970, 2021)]

# URLS = ["https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_1978"]

songs = []

with requests.Session() as session:
    for url in URLS:
        content = session.get(url).content
        soup = BeautifulSoup(content, "lxml")
        # The required table is always the 3rd table on the page
        table = soup.find_all("table", class_="wikitable")[2]
        rows = table.find_all("tr")

        for row in rows:
            try:
                data = row.find_all("td")
                '''must reference from the final entry in the row as some rows share the same first column,
                but this column is only present in the first of these rows'''
                artist = data[-4].text.replace("\n", "")
                
                single = data[-5].text
                if "/" in single:
                    singles = single.split("/")
                else:
                    singles = [single]

                for s in singles:
                    peak = data[-3].text.replace("\n", "")
                    peak_date = data[-2].text.replace("\n", "")
                    s = s.split("\"")[1]

                    songs.append(
                        {"artist": artist,
                        "title": s,
                        "peak": peak,
                        "date": peak_date})

            except Exception as e:
                continue

# This looks like a terribly inefficient way to do this, but it is a one-time thing that runs in about 10 seconds, so I will stick with it
dupes_removed = []
for i in range(len(songs)):
    if (songs[i]["artist"], songs[i]["title"]) not in [(songs[x]["artist"], songs[x]["title"]) for x in range(i+1, len(songs))]:
        dupes_removed.append(songs[i])

with open("all_top_10_singles_artist.json", "w", encoding="utf-8") as f:
    '''
    TODO: writing to the json without ensure_ascii=False makes the writer unable to write characters such as ö, even though they are ascii characters.
    '''
    f.write(json.dumps(dupes_removed, ensure_ascii=False, indent=2))
