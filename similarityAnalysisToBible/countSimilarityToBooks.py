#Count what Bible Verses are referenced the most often.
import pandas as pd

def countSimilarityToBooks(allWorksDF,similarVerses, outputFile):
    dicOfCounts = {}
    df=  pd.read_csv(allWorksDF)

    with open(similarVerses) as file:
        for line in file:
            l = line.strip().split("\t")
            if len(l)>1:
                for i in l[1:]:
                    book=df.iloc[int(i)]["Book"]
                    if book in dicOfCounts:
                        dicOfCounts[book]+=1
                    else:
                        dicOfCounts[book]=1

    print(len(dicOfCounts))
    sortedDic = dict(sorted(dicOfCounts.items(), key=lambda x:x[1], reverse=True))

    with open(outputFile, "w") as output:
        for k,v in sortedDic.items():
            output.write(f"{k}\t{v}\n")

allWorksDF= "standardWorksDF/allWorksDF"
similarVerses = "similarityAnalysisToBible/parsedSimilarVerses"
outputFile = "similarityAnalysisToBible/countOfMostReferencedBooks"
countSimilarityToBooks(allWorksDF,similarVerses, outputFile)