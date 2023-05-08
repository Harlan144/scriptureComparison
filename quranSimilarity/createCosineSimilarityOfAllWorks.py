import sys
sys.path.append("similarityAnalysisToBible")
from prepareSimilarVerseIndexforAnalysis import createCosineSimilarityFile


allTensons= "quranSimilarity/allWorksWithQuranTensor.pt"
outputFile = "allWorksSimilarVersesDepth100"
createCosineSimilarityFile(allTensons,allTensons,outputFile, similarVerseCount=100)
