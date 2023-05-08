import pandas as pd

allWorksDF= "standardWorksDF/allWorksDF"

df= pd.read_csv(allWorksDF)

df.value_counts(df["Book"]).to_csv("bookLength.csv")
