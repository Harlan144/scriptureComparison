#Normalizes the countOfReferencesByBomBook directory to the size of the Bible books. (needed for
#future Chi squared testing)
import scaleReferenceBooksByLength
import os

dir= "countOfReferencesByBomBook"
for fileName in os.listdir(dir):
    f= os.path.join(dir,fileName)
    outputFile = os.path.join("normalizedReferencesByBomBook",fileName)
    scaleReferenceBooksByLength.normalizeBookReferences(f,outputFile)
