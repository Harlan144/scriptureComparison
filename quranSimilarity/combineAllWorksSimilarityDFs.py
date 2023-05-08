#I'm not sure I'll end up using this combined parsed file, but it might be useful.

import pandas as pd
import os

inputFolder = "allWorksSimilarVerses0.85"
outputFile = "quranSimilarity/parsedAllWorks0.85"

df = pd.DataFrame()
with open(outputFile,"w") as output:

    for file in os.listdir(inputFolder):
        f = os.path.join(inputFolder, file)
        with open(f) as inputFile:
            for line in inputFile:
                output.write(line)
