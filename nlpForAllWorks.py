from sentence_transformers import SentenceTransformer, util
import pandas as pd
import re
import numpy as np
import torch
import heapq
model = SentenceTransformer('all-MiniLM-L6-v2')


# df = pd.read_csv("standardWorksDF/allDF")
# works = set(list(df['Work']))
# for work in works:
#     verses=  list(df.loc[df['Work'] == work]["CleanedVerse"])
#     allEmbeddings = model.encode(verses, convert_to_tensor=True, show_progress_bar=True)
#     fileName = work+"Tensor.pt"
#     torch.save(allEmbeddings, fileName)


#Sentences are encoded by calling model.encode()

tensorEmbeddingFiles = ["tensorEmbeddings/bomTensor.pt",
"tensorEmbeddings/dcTensor.pt",
"tensorEmbeddings/newtestamentTensor.pt",
"tensorEmbeddings/oldtestamentTensor.pt",
"tensorEmbeddings/pogpTensor.pt"]

newFiles = [
    "bomSimilarVerses",
    "dcSimilarVerses",
    "newTestSimilarVerses",
    "oldTestSimilarVerses",
    "pogpSimilarVerses",
]

allTensors = torch.load("tensorEmbeddings/tensor.pt")

for tensorIndex, tensorFile in enumerate(tensorEmbeddingFiles):
    oneBookEncoding = torch.load(tensorFile)
    cosine_scores = util.cos_sim(oneBookEncoding, allTensors)
    allTensorsLen = len(allTensors)
    print(cosine_scores.shape,len(oneBookEncoding), len(allTensors))
    versePairs = []
    for i in range(len(oneBookEncoding)):

        row = enumerate(cosine_scores[i])
        pairs = heapq.nlargest(6, row, key=lambda x: x[1])
        if pairs[0][1] > 0.999:
            pairs.pop(0)
        if len(pairs)==6:
            print(pairs)
            pairs.pop()
            print(pairs)
        versePairs.append({i:pairs})
        print(i, pairs)
    
    with open(newFiles[tensorIndex],"w") as outFile:
        for i in versePairs:
            outFile.write(str(i) +"\n")


#Print the embeddings
# cosine_scores = util.cos_sim(embeddings, embeddings)
# print(len(cosine_scores))
# versePairs = []

print("Writing to file...")

# with open("mostSimilarVerses","w") as outFile:
#     for i in range(len(cosine_scores)):
#         print(i)
#         pairs = []
#         for j in range(len(cosine_scores)):
#             if j!=i:
#                 pairs.append({'index': j, 'score': cosine_scores[i][j]})
                
#         pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)
#         versePairs.append({i:pairs[0:5]}) 
    
#     for i in versePairs:
#         outFile.write(str(i) +"\n")




# with open("verseWithEmbeddings", "w") as outFile:
#     for i, embedding in enumerate(embeddings):
#         outFile.write(f"{i}: {embedding}"+"\n")
