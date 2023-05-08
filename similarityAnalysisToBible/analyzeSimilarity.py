#Count what Bible Verses are referenced the most often.

def analyzeSimilarity(similarVerses,outputFile):
    dicOfCounts = {}

    with open(similarVerses) as file:
        for line in file:
            l = line.strip().split("\t")
            if len(l)>1:

                for i in l[1:]:
                    if i in dicOfCounts:
                        dicOfCounts[i]+=1
                    else:
                        dicOfCounts[i]=1

    print(len(dicOfCounts))
    sortedDic = dict(sorted(dicOfCounts.items(), key=lambda x:x[1], reverse=True))

    with open(outputFile, "w") as output:
        for k,v in sortedDic.items():
            output.write(f"{k}\t{v}\n")


similarVerses = "similarityAnalysisToBible/parsedSimilarVerses"
outputFile = "similarityAnalysisToBible/countOfMostReferencedVerses"
analyzeSimilarity(similarVerses,outputFile)