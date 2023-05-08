#https://github.com/risan/quran-json #TRIED, but the verses are jumbled sometimes.
#COMMENTED OUT BECAUSE IT IS ALREADY LOADED ONTO standardWorksJSON/quran.json

# url = "https://cdn.jsdelivr.net/npm/quran-json@3.1.2/dist/quran_en.json"

# with urllib.request.urlopen(url) as jsonUrl:
#     quranJSON = json.load(jsonUrl)

# with open('standardWorksJSON/quran.json', 'w') as outfile:
#     json.dump(quranJSON, outfile)


#I will try this with two English translations of the Quran (sourced from tanzil.net/). The first,
#by Talal Itani, is written in more simple English and uses "God" for "Allah".
#The second, by Saheeh International, is more well known and is one
# of the world's most popular Quran translations. It is biased towards Sunni orthodoxy
#https://en.wikipedia.org/wiki/Sahih_International

#https://tanzil.net/trans/en.sahih
#https://tanzil.net/trans/en.itani


import pandas as pd
import re


def quranFileToDF(quranFile, outputDF):
    regex = r"(\d+)\|(\d+)\|(.*)"
    quranList = []
    with open(quranFile) as file:
        for line in file:
            line =line.strip()
            if line[0].isdigit():
                parsedLine = re.findall(regex,line)
                if len(parsedLine)!=1:
                    print(line)
                else:
                    quranList.append(parsedLine[0])

            else:
                print(line)

    df= pd.DataFrame(quranList, columns= ["Chapter","VerseNum","Verse"])

    df.insert(0,'Book',"Quran")
    df.insert(0,'Work',"QuranTalalItani")

    clean_txt = []

    for w in range(len(df)):
        desc = df['Verse'][w].lower()

        #remove punctuation
        desc = re.sub('[^a-zA-Z]', ' ', desc)

        #remove tags
        desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)

        #remove digits and special chars
        desc=re.sub("(\\d|\\W)+"," ",desc)
        desc=re.sub("(\s+)+"," ",desc)
        clean_txt.append(desc)

    df['CleanedVerse'] = clean_txt
    print(df.head())

    df.to_csv(outputDF)


#quranFile = "standardWorksOLD/quranTalalItani"
#outputDF= "standardWorksDF/quranTalalItaniDF"
quranFile = "standardWorksOLD/quranSaheehInternational"
outputDF= "standardWorksDF/quranSaheehInternationalDF"
quranFileToDF(quranFile, outputDF)
