#Modify BOMSimilarityVerses so that it only contains values where cosSim>0.6 
#and the reference is in the Bible.

import re



def parseSimilarVerses(similarVerses,outputFile, cosSimCutoff=0.6, book=""):

    bookRangeDic= {"oldtest":(18215,41359), "newtest":(10258, 18214),
           "quran":(41995,48230), "bom":(0,6603),
            "dc":(6604,10257), "pogp":(41360,41994)}
    if not book:
        book = input("Which book of these: oldTest, newTest, quran, BOM, DC, or pogp ?")
    while book.lower() not in bookRangeDic.keys():
        book = input("Which book of these: oldTest, newTest, quran, BOM, DC, or pogp ?")
    
    bookRange= bookRangeDic[book] #Inclusive

    dic ={}
    with open(similarVerses) as file:
        for lineNum, line in enumerate(file):
            if lineNum>bookRange[1]:
                break
            elif lineNum>=bookRange[0]:
                line = line.strip()
                l = line.split("\t")
                index= l[0]
                val = l[1]
                val = val.lstrip("[").rstrip("]")
                pairs = val.split("), ")
                for i in pairs:
                    pair= i.lstrip("(")
                    indexOfVerse, similarityScore= pair.split(",")

                    similarityScore = float(re.findall(r"tensor\((\d+\.\d*)",similarityScore)[0])
                    indexOfVerse= int(indexOfVerse)
                    #print(indexOfVerse, similarityScore)

                    if similarityScore<cosSimCutoff: #make sure similarity score is high enough
                        break
                    
                    
                    if indexOfVerse < bookRange[0] or indexOfVerse>bookRange[1]: #not in BOM or DC or POGP
                        if index in dic:
                            dic[index].append(indexOfVerse)
                        else:
                            dic[index] = [indexOfVerse]

        with open(outputFile, "w") as output:
            for k,v in dic.items():
                output.write(f"{k}\t")
                for i in v:
                    output.write(f"{i}\t")
                output.write("\n")
            

# bomSimilarVerses = "similarityAnalysisToBible/bomSimilarVerses"
# outputFile = "similarityAnalysisToBible/parsedSimilarVerses"
# parseBOMSimilarVerses(bomSimilarVerses,outputFile,0.6)
bomSimilarVerses = "similarityAnalysisToBible/bomSimilarVerses"
outputFile = "syntenyAnalysis/similarVerses0.7"
parseBOMSimilarVerses(bomSimilarVerses,outputFile,0.7)
