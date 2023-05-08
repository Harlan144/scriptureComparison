import json
import pandas as pd
import re

#Found from https://github.com/bcbooks/scriptures-json/blob/master/pearl-of-great-price.json
f = open('standardWorksJSON/pearl-of-great-price.json')
file = json.load(f)
f.close()


dfList = []
book = ""
chapter = -1
verseNum = -1
for i in file["books"]:
    book = i["book"]
    for j in i["chapters"]:
        chapter = j["chapter"]
        for k in j["verses"]:
            verseNum = k["verse"]
            verse = k["text"]
            df2 = {
                    'Work': 'pearl of great price',
                    'Book':book,
                    'Chapter':chapter,
                    'VerseNum':verseNum,
                    'Verse': verse
            }
            dfList.append(df2)

df = pd.DataFrame(dfList)

clean_txt = []
for w in range(len(df)):
   desc = df['Verse'][w].lower()

   #remove punctuation
   desc = re.sub('[^a-zA-Z]', ' ', desc)

   #remove tags
   desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)

   #remove digits and special chars
   desc=re.sub("(\\d|\\W)+"," ",desc)
   clean_txt.append(desc)

df['CleanedVerse'] = clean_txt
#df = df.drop('Verse', axis=1)
df.to_csv("standardWorksDF/pogpDF")