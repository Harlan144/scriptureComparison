import pandas as pd

files = ["standardWorksDF/dcDF","standardWorksDF/newTestamentDF","standardWorksDF/oldTestamentDF","standardWorksDF/pogpDF","standardWorksDF/quranTalalItaniDF"]
finalDF = pd.read_csv("standardWorksDF/bomDF")
for file in files:
    df = pd.read_csv(file)
    finalDF= pd.concat([finalDF, df], ignore_index=True)

finalDF.rename(columns={"Unnamed: 0": "originalIndex"},inplace=True)
print(finalDF.head())
print(finalDF.tail())

finalDF.to_csv("standardWorksDF/allWorksWithQuranDF")