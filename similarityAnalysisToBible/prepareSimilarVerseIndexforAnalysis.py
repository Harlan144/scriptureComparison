from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import torch
import heapq

#Use pytorch to open the tensor files (NOT ON GITHUB- too large, please ask for them)
#and use those to find the cosine similarity for each verse of the BOM to all other standard works.
#In a seperate file (similarityAnalysisToBible/parseBOMSimilarityVerses.py),
# we will limit the similar verses.

model = SentenceTransformer('all-MiniLM-L6-v2')


def createCosineSimilarityFile(bomTensorFile,allTensorsFile,outputFile, similarVerseCount=15):

    allTensors = torch.load(allTensorsFile)
    bomEncoding = torch.load(bomTensorFile)
    cosine_scores = util.cos_sim(bomEncoding, allTensors)

    allTensorsLen = len(allTensors)

    print(cosine_scores.shape) #These should match
    print(len(bomEncoding), len(allTensors))

    versePairs = {}
    for i in range(len(bomEncoding)):
        print(i)
        row = enumerate(cosine_scores[i])
        pairs = heapq.nlargest(similarVerseCount, row, key=lambda x: x[1])
        for pair in pairs:
            index= pair[0]
            value = pair[1]
            if i in versePairs:
                versePairs[i].append((index,value))
            else:
                versePairs[i] = [(index,value)]


    with open(outputFile,"w") as outFile:
        for i,v in versePairs.items():
            outFile.write(f"{i}\t{str(v)}\n")


    print("Writing to file...")



#outputFile = "similarityAnalysisToBible/bomSimilarVersesDepth50"

#allTensors = "similarityAnalysisToBible/tensor.pt"
#bomTensorFile = "similarityAnalysisToBible/bomTensor.pt"
#createCosineSimilarityFile(bomTensorFile,allTensors,outputFile, 50)
