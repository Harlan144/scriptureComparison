#Instead of looking at the Book of Mormon as a whole and comparing its verses to the Bible 
#(to either Books or verses), it would be interesting to see how
#each author in the Book of Mormon tends to focus their message on different
#aspects of the gospel/Bible.
#To do this, this script combines aspects of:
#similarityAnalysisToBible/scaleReferenceBooksByLength.py
#similarityAnalysisToBible/analyzeSimilaritytoBooks.py
#and relies on bookLength.csv.
#In practice, I segment the Book of Mormon Books/Chapters by suspected authors, find the specific
#Books from the Bible that their message is most similar to, and compare that to the other verses.


#OK, time to backtrack. I can't easily identify which verse is written by which author, and even if
#I could, Mormon or Moroni abridged most of the Book, potentially overwritting their voices onto the
#original authors. Also, one must consider that Joseph Smith himself has his voice come through the
#Book of Mormon, irrelavent of the authors.

#Sooo, maybe I could try to run this analysis by Book in the Book of Mormon that is longer than x verses?
#I'm not sure how well this would work, but it'd be worth a try.

#All that to say, look at "similarityAnalysisToBible/analyzeSimilarityByBOMAuthor.py" instead.

