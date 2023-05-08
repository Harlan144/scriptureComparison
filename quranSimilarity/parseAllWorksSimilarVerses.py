import sys
sys.path.append("similarityAnalysisToBible")
from parseBOMSimilarityVerses import parseSimilarVerses
import os
similarVerseFile = "quranSimilarity/allWorksSimilarVersesDepth100"

outputFolder= "allWorksSimilarVerses0.85"
cosSimCutoff= 0.85

bookList = ["oldtest","newtest","quran","bom","dc","pogp"]
for book in bookList:
    outputFile = os.path.join(outputFolder, book+str(cosSimCutoff))
    parseSimilarVerses(similarVerseFile,outputFile, cosSimCutoff=cosSimCutoff, book=book)

