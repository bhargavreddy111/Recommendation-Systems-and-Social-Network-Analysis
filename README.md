# Social-Network-Analysis
Print Top 5 recommendations for books on Amazon using a composite score implementing network analysis concepts
Problem Definition

In this Project, I used Amazon Product Co-purchase data to make Book Recommendations using Network Analysis. This project covered 3 main aspects:
•	Apply Python concepts to read and manipulate data and get it ready for analysis
•	Apply Network Analysis concepts to Build and Analyze Graphs
•	Apply concepts in Text Processing, Network Analysis and Recommendation Systems to make a product recommendation


I used the Amazon Meta-Data Set maintained on the SNAP site. This data set is comprised of product and review metdata on 548,552 different products. The data was collected in 2006 by crawling the Amazon website. The following information is available for each product in the dataset:
•	Id: Product id (number 0, ..., 548551)
•	ASIN: Amazon Standard Identification Number. 
The Amazon Standard Identification Number (ASIN) is a 10-character alphanumeric unique identifier assigned by Amazon.com for product identification. We can lookup products by ASIN using following link: https://www.amazon.com/product-reviews/<ASIN> 
•	title: Name/title of the product
•	group: Product group. The product group can be Book, DVD, Video or Music.
•	salesrank: Amazon Salesrank
The Amazon sales rank represents how a product is selling in comparison to other products in its primary category. The lower the rank, the better a product is selling. 
•	similar: ASINs of co-purchased products (people who buy X also buy Y)
•	categories: Location in product category hierarchy to which the product belongs (separated by |, category id in [])
•	reviews: Product review information: total number of reviews, average rating, as well as individual customer review information including time, user id, rating, total number of votes on the review, total number of helpfulness votes (how many people found the review to be helpful)

 


