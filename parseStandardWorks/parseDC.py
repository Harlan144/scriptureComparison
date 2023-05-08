import json
import pandas as pd
import re

f = open('standardWorksJSON/dc.json')
file = json.load(f)
f.close()


dfList = []
book = "D&C"
chapter = -1
verseNum = -1
for i in file["sections"]:
    chapter = i["section"]
    for j in i["verses"]:
        verseNum = j["verse"]
        verse = j["text"]
        df2 = {
                'Work': 'd&c',
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
df.to_csv("standardWorksDF/dcDF")