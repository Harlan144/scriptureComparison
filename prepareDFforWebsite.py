import pandas as pd

df= pd.read_csv("standardWorksDF/allDF")

df.drop(columns=["CleanedVerse"], inplace=True)
df['Book'] = df['Book'].str.lower()
df.to_csv("standworksDFWebsite",index=False)