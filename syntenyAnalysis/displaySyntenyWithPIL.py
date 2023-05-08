from PIL import Image, ImageDraw 
import pandas as pd




allWorks = "standardWorksDF/allWorksDF"
parsedBomReferences = "syntenyAnalysis/similarVerses0.9"
outputSyntenyPlot= "syntenyAnalysis/figPIL.png"

allWorksDF= pd.read_csv(allWorks)

oldTestDF = allWorksDF[(allWorksDF["Work"]=="old testament")]
newTestDF= allWorksDF[(allWorksDF["Work"]=="new testament")]
oldTestamentLen = len(oldTestDF)
newTestamentLen = len(newTestDF)

bibleLen = len(allWorksDF[(allWorksDF["Work"]=="old testament") | (allWorksDF["Work"]=="new testament")])
bomLen = len(allWorksDF[(allWorksDF["Work"]=="book of mormon")])


sizeMultiplier= bibleLen/bomLen

bookHeight= max(bibleLen,bomLen)//20
distanceBetweenBooks=bookHeight*2
bibleWidth = bibleLen

bomWidth = bibleLen #But the points will be affected by sizeMultiplier
print(bomWidth,bibleWidth)

bomTopLeft = (0,0)

#bibleTopLeft = (0,bookHeight+distanceBetweenBooks)
#bible = plt.Rectangle(bibleTopLeft, bibleWidth, bookHeight, fc='blue',ec="red")
#plt.gca().add_patch(bible)

img = Image.new("RGBA", (int(bibleWidth*1.2),int(bibleWidth*0.3)))
draw = ImageDraw.Draw(img)

oldTestx0 = 0
oldTestx1= oldTestx0+oldTestamentLen
oldTesty0=bookHeight+distanceBetweenBooks
oldTesty1=oldTesty0+bookHeight
oldTestament = draw.rectangle((oldTestx0, oldTesty0, oldTestx1,oldTesty1), outline='teal', fill='orange')


distBetweenNewAndOldTestament = bibleLen/10
newTestx0=distBetweenNewAndOldTestament+oldTestamentLen
newTestx1=newTestx0+newTestamentLen
newTesty0=bookHeight+distanceBetweenBooks
newTesty1=newTesty0+bookHeight

newTestament = draw.rectangle((newTestx0, newTesty0, newTestx1, newTesty1), outline='teal', fill='green')
bom = draw.rectangle((0,0, bomWidth, bookHeight), outline='teal', fill='red')


#Only include names with at least 100 verses
minBookLen = 200
newTestByBooks= newTestDF["Book"].value_counts().loc[lambda x:x>minBookLen]
limitedNewTestBooks = list(newTestByBooks.index)
oldTestByBooks= oldTestDF["Book"].value_counts().loc[lambda x:x>minBookLen] 
limitedOldTestBooks = list(oldTestByBooks.index)
bomByBooks= allWorksDF[allWorksDF["Work"]=="book of mormon"]["Book"].value_counts().loc[lambda x:x>minBookLen] 
limitedBomBooks = list(bomByBooks.index)


newTestBookRanges = {}
for book in limitedNewTestBooks:
    indicies = allWorksDF[(allWorksDF["Book"]==book)].index
    indexRange = (indicies[0],indicies[-1])
    newTestBookRanges[book]= indexRange

oldTestBookRanges = {}
for book in limitedOldTestBooks:
    indicies = allWorksDF[(allWorksDF["Book"]==book)].index
    indexRange = (indicies[0],indicies[-1])
    oldTestBookRanges[book]= indexRange

bomBookRanges = {}
for book in limitedBomBooks:
    indicies = allWorksDF[(allWorksDF["Book"]==book)].index
    indexRange = (indicies[0],indicies[-1])
    bomBookRanges[book]= indexRange

# for book, indexRange in oldTestBookRanges.items():
#     xPos = (indexRange[0]+indexRange[1])//2 - 18215
#     draw.text(xPos, 2*bookHeight+distanceBetweenBooks, book, ha='left', rotation=90, wrap=True, fontsize='xx-small')

# for book, indexRange in newTestBookRanges.items():
#     xPos = (indexRange[0]+indexRange[1])//2 -10258+oldTestamentLen+distBetweenNewAndOldTestament 
#     draw.text(xPos, 2*bookHeight+distanceBetweenBooks, book, ha='left', rotation=90, wrap=True, fontsize='xx-small')

# for book, indexRange in bomBookRanges.items():
#     xPos = int(((indexRange[0]+indexRange[1])/2)*sizeMultiplier)
#     draw.text(xPos, 0, book, ha='left', rotation=90, wrap=True, fontsize='xx-small')


with open(parsedBomReferences) as file:
    for line in file:
        l = line.strip().split("\t")
        bomVerseNum = int(l[0]) 

        for bestBibleVerseNum in l[1:]:
            bestBibleVerseNum = int(bestBibleVerseNum)
            #If in new testament (based on order in AllWorksDF)
            if bestBibleVerseNum>=10258 and bestBibleVerseNum<18215:
                #In new testament
                bestBibleVerseNum=bestBibleVerseNum-10258+oldTestamentLen+distBetweenNewAndOldTestament 
            else:
                bestBibleVerseNum-=18215 #In old testament

            line = draw.line([(int(bomVerseNum*sizeMultiplier), bookHeight),
                               (bestBibleVerseNum, bookHeight+distanceBetweenBooks)],width=2)
                






img.save(outputSyntenyPlot)