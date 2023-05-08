import pandas as pd
import re
dfList = []

with open("bom") as file:
    book = ""
    chapter = ""
    verseNum = -1
    verse = []
    for line in file:
        line = line.strip()
        if line:
            l = line.split()
            if "Chapter" in l:
                chapterIndex= l.index("Chapter")
                book = " ".join(l[:chapterIndex])
                print(book)
                chapter = l[chapterIndex+1]
                print(chapter)
            elif ":" in l[0]:
                #check chapter:
                chapAndVerse = l[0].split(":")
                if chapAndVerse[0].isdigit():
                    if chapAndVerse[0] != chapter:
                        print("Ya goofed!", line)
                    verseNum = chapAndVerse[1]
                    verse.extend(l[1:])
            else:
                verse.extend(l)

        else: #if the line is blank
            if verse:
                df2 = {'Work': 'book of mormon',
                    'Book':book.lower(),
                    'Chapter':chapter,
                    'VerseNum':verseNum,
                    'Verse': " ".join(verse)
                }
                dfList.append(df2)
            
            verse = []

df = pd.DataFrame(dfList)
df.to_csv("AllWorksForWebsite")