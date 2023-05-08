import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
import numpy as np



def syntenyGraph(allWorks,parsedBomReferences,outputSyntenyPlot, minBookLen=200,cosineThreshold="0.9"):

    allWorksDF= pd.read_csv(allWorks)

    oldTestDF = allWorksDF[(allWorksDF["Work"]=="old testament")]
    newTestDF= allWorksDF[(allWorksDF["Work"]=="new testament")]
    oldTestamentLen = len(oldTestDF)
    newTestamentLen = len(newTestDF)

    bibleLen = len(allWorksDF[(allWorksDF["Work"]=="old testament") | (allWorksDF["Work"]=="new testament")])
    bomLen = len(allWorksDF[(allWorksDF["Work"]=="book of mormon")])



    bookHeight= max(bibleLen,bomLen)//50
    distanceBetweenBooks=bookHeight*10



    #bibleTopLeft = (0,bookHeight+distanceBetweenBooks)
    #bible = plt.Rectangle(bibleTopLeft, bibleWidth, bookHeight, fc='blue',ec="red")
    #plt.gca().add_patch(bible)
    plt.axes()


    oldTestTopLeft = (0, bookHeight+distanceBetweenBooks)
    oldTestament = plt.Rectangle(oldTestTopLeft, oldTestamentLen, bookHeight, fc='gray',ec="black",lw=0.5)


    distBetweenNewAndOldTestament = bibleLen/10
    newTestTopLeft = (distBetweenNewAndOldTestament+oldTestamentLen, bookHeight+distanceBetweenBooks)
    newTestament = plt.Rectangle(newTestTopLeft, newTestamentLen, bookHeight, fc='gray',ec="black",lw=0.5)

    sizeMultiplier= (bibleLen+distBetweenNewAndOldTestament)/bomLen
    bomWidth = bibleLen #But the points will be affected by sizeMultiplier
    bomTopLeft = (0,0)
    bom = plt.Rectangle(bomTopLeft, bomWidth, bookHeight, fc='gray',ec="black",lw=0.5)

    plt.gca().add_patch(newTestament)
    plt.gca().add_patch(oldTestament)
    plt.gca().add_patch(bom)

    titleText= "Synteny Analysis of Similarity between the Book of Mormon and the Bible"
    subTitleText = "Calculated At "+cosineThreshold +" cosine similarity threshold"
    centerX= (bibleLen+distBetweenNewAndOldTestament)//2
    plt.text(centerX,3*(2*bookHeight+distBetweenNewAndOldTestament), titleText, ha='center', rotation=0, wrap=True, fontsize=15)
    plt.text(centerX,2.5*(2*bookHeight+distBetweenNewAndOldTestament), subTitleText, ha='center', rotation=0, wrap=True, fontsize=8)

    #Only include names with at least 100 verses
    newTestByBooks= newTestDF["Book"].value_counts(sort=False).loc[lambda x:x>minBookLen]
    limitedNewTestBooks = list(newTestByBooks.index)
    oldTestByBooks= oldTestDF["Book"].value_counts(sort=False).loc[lambda x:x>minBookLen] 
    limitedOldTestBooks = list(oldTestByBooks.index)
    bomByBooks= allWorksDF[allWorksDF["Work"]=="book of mormon"]["Book"].value_counts(sort=False).loc[lambda x:x>minBookLen] 

    limitedBomBooks = list(bomByBooks.index)

    colorTotal = len(limitedBomBooks)+len(limitedNewTestBooks)+len(limitedOldTestBooks)
    color = iter(cm.rainbow(np.linspace(0, 1, colorTotal)))


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

    for book, indexRange in oldTestBookRanges.items():
        c = next(color)

        bookLen= (indexRange[1]-indexRange[0])
        xPos = (indexRange[1]+indexRange[0])//2- 18215
        plt.text(xPos, 2.25*bookHeight+distanceBetweenBooks, book, ha='left', rotation=90, wrap=True, fontsize=4)
        x0= indexRange[0]-18215
        oldTestamentBook = plt.Rectangle((x0,bookHeight+distanceBetweenBooks), bookLen, bookHeight, fc=c,ec="black",lw=0.5)
        plt.gca().add_patch(oldTestamentBook)


    for book, indexRange in newTestBookRanges.items():
        c = next(color)
        bookLen= (indexRange[1]-indexRange[0])

        xPos = (indexRange[0]+indexRange[1])//2 -10258+oldTestamentLen+distBetweenNewAndOldTestament 
        plt.text(xPos, 2.25*bookHeight+distanceBetweenBooks, book, ha='left', rotation=90, wrap=True, fontsize=4)
        x0= indexRange[0]-10258+oldTestamentLen+distBetweenNewAndOldTestament
        newTestamentBook = plt.Rectangle((x0,bookHeight+distanceBetweenBooks), bookLen, bookHeight, fc=c,ec="black",lw=0.5)
        plt.gca().add_patch(newTestamentBook)

    for book, indexRange in bomBookRanges.items():
        c = next(color)

        bookLen = int((indexRange[1]-indexRange[0])*sizeMultiplier)
        xPos = int(((indexRange[0]+indexRange[1])/2)*sizeMultiplier)
        plt.text(xPos, -0.25*bookHeight, book, ha='left', rotation=-90, wrap=True, fontsize=4)
        x0= int(indexRange[0]*sizeMultiplier)
        bomBook = plt.Rectangle((x0,0), bookLen, bookHeight, fc=c,ec="black",lw=0.5)
        plt.gca().add_patch(bomBook)



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

                line = plt.Line2D((int(bomVerseNum*sizeMultiplier), bestBibleVerseNum),
                                (bookHeight,bookHeight+distanceBetweenBooks), linewidth=0.1)
                plt.gca().add_line(line)





    plt.axis('scaled')
    plt.axis('off')
    plt.savefig(outputSyntenyPlot,dpi=1200)

allWorks = "standardWorksDF/allWorksDF"
parsedBomReferences = "syntenyAnalysis/similarVerses0.8"
outputSyntenyPlot= "syntenyAnalysis/figsimilarity0dot8"

syntenyGraph(allWorks,parsedBomReferences,outputSyntenyPlot, minBookLen=150,cosineThreshold='0.8')