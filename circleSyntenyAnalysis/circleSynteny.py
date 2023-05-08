import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import matplotlib.path as mpath
from matplotlib.pyplot import cm
import pandas as pd
import numpy as np
import math


def findPosBasedOnAngle(angle, radius): #counterClockwise?
    #sohcahtoa
    radianAngle= math.radians(angle)
    x=math.cos(radianAngle)*radius
    y= math.sin(radianAngle)*radius
    return x,y


def circleSyntenyGraph(allWorks,parsedReferenceFile, outputSyntenyPlot, includeOnlyFirst =False,minBookLen=200,cosineThreshold="0.8"):
    plt.axes()
    Path= mpath.Path

    allWorksDF= pd.read_csv(allWorks)

    totalVerseCount = len(allWorksDF)

    worksAndLens = allWorksDF["Work"].value_counts(sort=False)

    totalWorkCount = len(worksAndLens)
    degreeBetweenWorks = 2

    anglePerVerse= (360-degreeBetweenWorks*totalWorkCount)/(totalVerseCount) 

    workIndexes ={}
    for work,length in worksAndLens.items():
        #only get the first?
        firstIndex =allWorksDF.loc[allWorksDF["Work"]==work].index[0]
        lastIndex = firstIndex+length #NOT INCLUSIVE
        workIndexes[work]= (firstIndex,lastIndex)
        
    currentAngle =0
    workAngles= {}
    for work, indexRange in workIndexes.items():
        endAngle = currentAngle+(indexRange[1]-indexRange[0])*anglePerVerse
        workAngles[work]= (currentAngle,endAngle)
        currentAngle =endAngle+degreeBetweenWorks

    centerOfGraph = (0,0)
    circleDiameter= totalVerseCount/math.pi #about 2pi, this doesn't need to be exact.
    circleRadius =circleDiameter/2
    booksInWorks = {}
    totalBooks = 0
    for work in workIndexes:
        books= allWorksDF[allWorksDF["Work"]==work]["Book"].value_counts(sort=False).loc[lambda x:x>minBookLen]
        limitedBooks = list(books.index)
        totalBooks+=len(limitedBooks)
        booksInWorks[work]=limitedBooks
    
    bookAngles= {}
    for work,bookList in booksInWorks.items():
        angleOfWork = workAngles[work]
        totalAngle = angleOfWork[1]-angleOfWork[0]
        indexOfWork = workIndexes[work]
        workLen = indexOfWork[1]-indexOfWork[0]
        for book in bookList:
            bookDF =allWorksDF.loc[allWorksDF["Book"]==book].index
            firstIndex = bookDF[0]
            lastIndex = bookDF[-1]
            startingAngle = (firstIndex-indexOfWork[0])/workLen*totalAngle+angleOfWork[0]
            endingAngle=(lastIndex-indexOfWork[0])/workLen*totalAngle+angleOfWork[0]
            if work in bookAngles:
                bookAngles[work][book] = (startingAngle,endingAngle)
            else:
                bookAngles[work]= {book:(startingAngle,endingAngle)}



    color = iter(cm.rainbow(np.linspace(0, 1, totalBooks)))

    for work, angles in workAngles.items():
        arc= mpatch.Arc(centerOfGraph,
                width = circleDiameter,
                height= circleDiameter,
                angle= 0,
                theta1= angles[0],
                theta2= angles[1],
                linewidth=5,
                ec="gray"
        )
        plt.gca().add_patch(arc)
        textAngle = (angles[1]+angles[0])/2
        textX, textY= findPosBasedOnAngle(textAngle,circleRadius*1.3)

        workNames = {"QuranTalalItani":"Qur'an","pearl of great price":"Pearl of Great Price",
                     "old testament": "Old Testament","book of mormon":"Book of Mormon",
                     "d&c":"Doctrine and Covenants", "new testament":"New Testament"
        }
        if textAngle<180:
            plt.text(textX, textY, workNames[work], ha='center', rotation=textAngle-90, wrap=True, fontsize=7)
        else:
            plt.text(textX, textY, workNames[work], ha='center', rotation=textAngle+90, wrap=True,fontsize=7)


    for work, bookDic in bookAngles.items():
            for book, bookAngles in bookDic.items():
                c = next(color)

                arc= mpatch.Arc(centerOfGraph,
                        width = circleDiameter,
                        height= circleDiameter,
                        angle= 0,
                        theta1= bookAngles[0],
                        theta2= bookAngles[1],
                        linewidth=5,
                        ec=c
                )
                plt.gca().add_patch(arc)
                textAngle = (bookAngles[1]+bookAngles[0])/2
                textX, textY= findPosBasedOnAngle(textAngle,circleRadius*1.03)
                plt.text(textX, textY, book, ha='left', rotation=textAngle, wrap=True, fontsize=3)


    def findPosFromVerseNum(verseNum):
        for work,workRange in workIndexes.items():
            if verseNum>=workRange[0] and verseNum<workRange[1]:
                #it is in that book.
                workLen =workRange[1]-workRange[0]
                workAngleRange = workAngles[work]
                angleTotal = workAngleRange[1]-workAngleRange[0]
                fractionThroughWork = (verseNum-workRange[0])/workLen

                verseAngle= workAngleRange[0]+fractionThroughWork*angleTotal
                versePoint= findPosBasedOnAngle(verseAngle,circleRadius*0.98)
                return versePoint

    with open(parsedReferenceFile) as file:
        for line in file:
            l = line.strip().split("\t")
            
            verseNum = int(l[0])
            versePoint = findPosFromVerseNum(verseNum)
            if includeOnlyFirst:
                secondVerse= int(l[1])
                verse2Point = findPosFromVerseNum(secondVerse)
                bezierCurve = mpatch.PathPatch(Path([versePoint,(0,0),verse2Point],
                                                [Path.MOVETO,Path.CURVE3,Path.CURVE3]),
                                                fc="none", linewidth=0.1)
                plt.gca().add_patch(bezierCurve)
            else:
                for secondVerse in l[1:]:
                    secondVerse= int(secondVerse)
                    verse2Point = findPosFromVerseNum(secondVerse)

                    bezierCurve = mpatch.PathPatch(Path([versePoint,(0,0),verse2Point],
                                                    [Path.MOVETO,Path.CURVE3,Path.CURVE3]),
                                                    fc="none", linewidth=0.1)
                                                
                    plt.gca().add_patch(bezierCurve)
                


    plt.axis('scaled')
    plt.axis('off')
    plt.savefig(outputSyntenyPlot,dpi=1200)


allWorks = "standardWorksDF/allWorksWithQuranDF"
parsedReferenceFile = "quranSimilarity/parsedAllWorks0.85"
outputSyntenyPlot= "circleSyntenyAnalysis/newtest0dot85"

circleSyntenyGraph(allWorks,parsedReferenceFile,outputSyntenyPlot,includeOnlyFirst=False,minBookLen=150)