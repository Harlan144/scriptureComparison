#Given a file with the count of the most referenced Bible books, normalize that according to
#the length of the Bible books in verses. Otherwise, Psalms is almost always the top.
#Output this into a seperate file.

import pandas as pd

def normalizeBookReferences(referencedBooks,outputNormalizedDF):
    bookLength = "bookLength.csv"
    df= pd.read_csv(bookLength)
    df.rename(columns={"0":"verseCount"},inplace=True)
    dic= dict(zip(df["Book"],df["verseCount"]))

    dfReferences = pd.read_csv(referencedBooks,sep="\t", header=None)
    dfReferences.rename(columns={0:'Book',1:"RefCount"},inplace=True)
    print(dfReferences.columns)
    print(dfReferences.head())

    newDF = pd.merge(dfReferences,df,how="inner",on="Book")
    newDF["NormalizedReference"] = newDF["RefCount"]/newDF["verseCount"]
    sortedNormalizedDF = newDF.sort_values("NormalizedReference",ascending=False)


    sortedNormalizedDF.to_csv(outputNormalizedDF, index=False)




referencedBooks ="similarityAnalysisToBible/countOfMostReferencedBooks"
outputNormalizedDF = "similarityAnalysisToBible/normalizedCountOfReferencedBooks"
normalizeBookReferences(referencedBooks, outputNormalizedDF)