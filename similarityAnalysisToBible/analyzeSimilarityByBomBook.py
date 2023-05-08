import pandas as pd
import os


#Limit the verses to only those from books in the Book of Mormon with >100 verses.
similarVersesToBOM = "similarityAnalysisToBible/parsedSimilarVerses"
bomDF = pd.read_csv("standardWorksDF/bomDF")
bomByBooks= bomDF["Book"].value_counts().loc[lambda x:x>100] #Need at least 100 verses.?

#Check to see which books are left.
limitedBooks = list(bomByBooks.index)
print(limitedBooks)

#Find the range of these Books in the bomDF.
bookRanges = {}
for book in limitedBooks:
    indicies = bomDF[(bomDF["Book"]==book)].index
    indexRange = (indicies[0],indicies[-1])
    bookRanges[book]= indexRange


#Separate the verses from each book into a dictionary. keys= Books, values= Bible references
referencesByBooks = {}
with open(similarVersesToBOM) as file:
    for line in file:
        l = line.split("\t")
        bomIndex = int(l[0])
        for book,indexRange in bookRanges.items():
            if bomIndex>=int(indexRange[0]) and bomIndex<=int(indexRange[1]):
                if book in referencesByBooks:
                    referencesByBooks[book].append(line)
                else:
                    referencesByBooks[book]= [line]
                
                break


#Write this dictionary of references by BOM Book into their own files in the outputDir.
outputDir = "similarityByBOMBook"
for book, listOfRef in referencesByBooks.items():
    newFilePath = outputDir+"/"+book
    with open(newFilePath,"w") as file:
        for refLine in listOfRef:
            file.write(refLine)



allWorksDF= "standardWorksDF/allWorksDF"
df=  pd.read_csv(allWorksDF)

#Now iterate through these files we created, and figure out which Bible book each reference corresponds to.
#This is very similar to analyisSimilaritytoBooks.py
for filename in os.listdir(outputDir):
    f = os.path.join(outputDir, filename)

    dicOfCounts = {}
    with open(f) as file:
        for line in file:
            l = line.strip().split("\t")
            if len(l)>1:

                for i in l[1:]:
                    bibleBook= df.iloc[int(i)]["Book"]
                    if bibleBook in dicOfCounts:
                        dicOfCounts[bibleBook]+=1
                    else:
                        dicOfCounts[bibleBook]=1

    sortedDic = dict(sorted(dicOfCounts.items(), key=lambda x:x[1], reverse=True))
    
    #Take this sorted dictionary of the reference counts by Bible books and write it into their own
    #files in its directory.
    countByBooksDir = "countOfReferencesByBomBook"
    outputFile= os.path.join(countByBooksDir,filename+"CountOfReferencedBooks")
    print(outputFile)
    with open(outputFile, "w") as output:
        for k,v in sortedDic.items():
            output.write(f"{k}\t{v}\n")

