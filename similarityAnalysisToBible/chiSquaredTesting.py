#Would a Chi-squared test work to see if the Book of Mormon cites books from the Bible at different
#frequencies? Intuition says yes, but I'd love a stat-expert to confirm this!
#Null hypothesis- BOM randomly cites verses from the Bible (Cos sim limit = 0.6)

import pandas as pd

def calculate_chi_square_part(obv, exp):
    return ((obv-exp)**2)/exp



normalizedRefCount= "similarityAnalysisToBible/normalizedCountOfReferencedBooks"

normalizedDF= pd.read_csv(normalizedRefCount)
totalRefs = sum(normalizedDF["RefCount"])
totalVerses = sum(normalizedDF["verseCount"])
refPerVerse= totalRefs/totalVerses
normalizedDF["expectedRef"] = normalizedDF["verseCount"]*refPerVerse

normalizedDF["indvChiSquare"] = calculate_chi_square_part(normalizedDF["RefCount"],normalizedDF["expectedRef"])


chiSquaredValue=  sum(normalizedDF["indvChiSquare"])
print("Degrees of freedom: ",len(normalizedDF["indvChiSquare"])-1)
print("Actual value: ",chiSquaredValue)



###PART 2 ###
#See if it is significant by the Book of Mormon Book.
#############


similarVersesToBOM = "similarityAnalysisToBible/parsedSimilarVerses" #chi square of 0.6
bomDF = pd.read_csv("standardWorksDF/bomDF")
bomByBooks= list(bomDF["Book"].value_counts(sort="False").index)


#Find the range of these Books in the bomDF.
bookRanges = {}
for book in bomByBooks:
    indicies = bomDF[(bomDF["Book"]==book)].index
    indexRange = (indicies[0],indicies[-1])
    bookRanges[book]= indexRange


#Separate the verses from each book into a dictionary. keys= Books, values= count of references
referenceCountByBook = {}

for book in bomByBooks:
    referenceCountByBook[book]=[0,bookRanges[book][1]-bookRanges[book][0]+1]

with open(similarVersesToBOM) as file:
    for line in file:
        l = line.strip().split("\t")
        bomIndex = int(l[0])
        for book,indexRange in bookRanges.items():
            if bomIndex>=int(indexRange[0]) and bomIndex<=int(indexRange[1]):
                referenceCountByBook[book][0]+=len(l[1:]) #add all references???
                break

bomRefCountDF = pd.DataFrame.from_dict(referenceCountByBook, orient='index', columns=["RefCount","BookLen"])
totalBOMVerses = 6604
refPerBOMVerse= totalRefs/totalBOMVerses

bomRefCountDF["ExpRefPerBook"] = refPerBOMVerse*bomRefCountDF["BookLen"]

bomRefCountDF["ChiSquare"]=calculate_chi_square_part(bomRefCountDF["RefCount"],bomRefCountDF["ExpRefPerBook"])
chiSquareBOM = sum(bomRefCountDF["ChiSquare"])
print("Degrees of freedom: ",len(bomRefCountDF["ChiSquare"])-1)
print("Actual value: ",chiSquareBOM)

#BOTH ARE SIGNIFICANT