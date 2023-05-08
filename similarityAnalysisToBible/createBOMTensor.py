#Create bomTensor.py from bomDF.

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')
df = pd.read_csv("standardWorksDF/bomDF")


verses=  list(df["CleanedVerse"])

allEmbeddings = model.encode(verses, convert_to_tensor=True, show_progress_bar=True)
torch.save(allEmbeddings, "similarityAnalysisToBible/bomTensor.pt")