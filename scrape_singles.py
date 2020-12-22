import requests
from bs4 import BeautifulSoup
import json

URLS = [
    f"https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_{year}" for year in range(1970, 2021)]

# URLS = ["https://en.wikipedia.org/wiki/List_of_UK_top-ten_singles_in_1978"]

song_dict = dict()

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
                artist = data[-4].text
                artist = artist.replace("\n", "")
                
                single = data[-5].text
                if "/" in single:
                    singles = single.split("/")
                else:
                    singles = [single]

                for s in singles:
                    s = s.split("\"")[1]
                    
                    # Some singles that repeat have different capitalisation, so the search must be case insensitive
                    if s.lower() in (x.lower() for x in song_dict.keys()):
                        if artist.lower() in (x.lower() for x in song_dict[s]):
                            continue
                        else:
                            song_dict[s].append(artist)
                    else:
                        song_dict[s] = [artist]

            except Exception as e:
                continue


with open("all_top_10_singles_artist.json", "w", encoding="utf-8") as f:
    '''
    TODO: writing to the json without ensure_ascii=False makes the writer unable to write characters such as ö, even though they are ascii characters.
    '''
    f.write(json.dumps(song_dict, ensure_ascii=False, indent=2))
