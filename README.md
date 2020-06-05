# Social-Network-Analysis
Print Top 5 recommendations for books on Amazon using a composite score implementing network analysis concepts
Problem Definition

In this Project, I used Amazon Product Co-purchase data to make Book Recommendations using Network Analysis. This project covered 3 main aspects:
•	Apply Python concepts to read and manipulate data and get it ready for analysis
•	Apply Network Analysis concepts to Build and Analyze Graphs
•	Apply concepts in Text Processing, Network Analysis and Recommendation Systems to make a product recommendation


Procedure followed by me:
•	Firstly, I have imported all the packages necessary, then I read the data from “amazon-books.csv”, read the data from amazon-books-copurchase.adjlist and assigned it to “copurchaseGraph”
•	Assumed that person is choosing to buy a certain book, then got its metadata based on its “ASIN”
Step1: Got the depth-1 ego network of purchased Asin 
Step2: Retained only that books that have similarity to purchased Asin based on threshold=0.5
Step3: Got the list of nodes associated with purchased Asin after step 2
Step 4: 
1)	Firstly there are certain rows in “amazonBooks” dataframe where the salesrank was 0 or negative values. I removed all the observations which had these unrealistic salesranks
2)	Then I normalized “AvgRatings”, “ClusteringCoeff”,”DegreeCentrality”,”TotalReviews” columns using minmax scaler.
3)	Then I transformed SalesRank column using a custom function. Ths custom function performed log(Max(salesrank)/salesrank). Salesrank values can take very big values hence I used log normal function.
4)	Then I defined the composite score as: 
                  Score= Normalized AvgRating*Normalized Degree Centrality*Normalized TotalReviews* log(Max(salesrank)/salesrank)

Reason for the logic of composite score:
(a)	If a copurchase Book has higher avg rating, it is natural that customer would be more inclined to buy that than something which has lower avg rating
(b)	If a copurchase Book has higher Degree Centrality, it means that book is associated with purchases of so many other books which implies that higher the degree centrality, more popular that book is. So it is reasonable to assume that customer would be more inclined to buy a book with higher Degree Centrality than something which has lower Degree Centrality
(c)	If a copurchase book has high “Total reviews” then it implies that the avg rating that book is a result of the reviews given by large number of customers which adds more credibility to the rating. A book which has 4.5 Rating with 500 reviews is more credible than a book that has 4.5 rating with 50 reviews.  In addition, high “Total reviews” is also a latent measure of popularity among customers.
(d)	If a copurchase book has high sales rank, it means is bought less frequently than a book which has low sales rank. So the score become inversely proportional to salesrank. There is an issue of large values that could appear as SalesRank, so this is dealt by using log function on the inverse of normalized sale rank value.
(e)	I haven’t included clustering coefficient in the calculation of composite score as I felt it wont reflect the buying confidence properly. It is natural that a copurchase book which has high degree of centrality(say 60) has very few connected books that are copurchased which leads to low clustering coefficient. On the other hand, a book which has degree of centrality ‘2’ has very large chance that its connected books are copurchased between them leading to high clustering coefficient. But it doesn’t mean that customer choses the latter one as that book is not popular at all even though it’s clustering coefficient is high enough.
Step 5: Once I got the composite scores for each of the copurchase books, then I sorted the list to get top 5 Asin’s if that scores list had more than 5 copurchase books. If that list had less than 5 copurchase books, I recommended as many copurchases as are available in the final recommendations
Step6: Once I got the top 5 ASIN’s to be recommended I used the metadata to print “Title”, “SalesRank”,”TotalReviews”,”AvgRating”,”DegreeCentrality” and “ClusteringCoefficient”

