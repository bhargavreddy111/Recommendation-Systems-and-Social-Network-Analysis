import networkx
from operator import itemgetter
import matplotlib.pyplot
import pandas as pd

# Loading the data from amazon-books.csv into amazonBooks dataframe;
amazonBooks = pd.read_csv('./amazon-books.csv', index_col=0)

# getting the data from amazon-books-copurchase.adjlist;
# assigned it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Assuming a person is considering buying the following book;
# the idea is to see what else can be recommended to them based on copurchase behavior 
# seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# First, I try to get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks.loc[purchasedAsin,'Title'])
print ("SalesRank = ", amazonBooks.loc[purchasedAsin,'SalesRank'])
print ("TotalReviews = ", amazonBooks.loc[purchasedAsin,'TotalReviews'])
print ("AvgRating = ", amazonBooks.loc[purchasedAsin,'AvgRating'])
print ("DegreeCentrality = ", amazonBooks.loc[purchasedAsin,'DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks.loc[purchasedAsin,'ClusteringCoeff'])
    

# looking at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
#  I Get the depth-1 ego network of purchasedAsin from copurchaseGraph,
#     and assign the resulting graph to purchasedAsinEgoGraph.
purchasedAsinEgoGraph = networkx.Graph()
purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph, purchasedAsin, radius=1)


# Now edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So I used the
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
# 
#   Using the island method on purchasedAsinEgoGraph to only retain edges with 
#     threshold >= 0.5, and then assign the resulting graph to purchasedAsinEgoTrimGraph
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f, t, e in purchasedAsinEgoGraph.edges(data=True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t,weight=e['weight'])


# With the purchasedAsinEgoTrimGraph I constructed above, 
# I can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
# #    After finding the list of neighbors of the purchasedAsin in the 
#     purchasedAsinEgoTrimGraph, I then assigned it to purchasedAsinNeighbors
purchasedAsinNeighbors = []
purchasedAsinNeighbors = [i for i in purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)] 
print (purchasedAsinNeighbors)

# Now I try to pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
# (4) #     I have created a composite measure to make Top Five book 
#     recommendations based on the following metrics associated 
#     with nodes in purchasedAsinNeighbors: SalesRank, AvgRating, 
#     TotalReviews, DegreeCentrality, and ClusteringCoeff. 
#     #   Also, the data is transformed appropriately using 
#     sklearn preprocessing so the composite measure isn't overwhelmed 
#     by measures which are on a higher scale.

#Removing rows where sales rank is less than 1 as it doesnt make sense
import numpy as np
amazonBooks=amazonBooks[~(amazonBooks['SalesRank']<1)]
numericvars = ['AvgRating', 'ClusteringCoeff','DegreeCentrality','TotalReviews']
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
amazonBooks_norm = pd.DataFrame(mms.fit_transform(amazonBooks[numericvars]), columns=['mms_'+x for x in numericvars], index=
amazonBooks.index)
amazonBooks_norm = pd.concat([amazonBooks, amazonBooks_norm], axis=1)
amazonBooks_norm = amazonBooks_norm.drop(numericvars, axis=1)
amazonBooks_norm.head()

def func(df):
    x=np.log(df.max()/df)
    return x
from sklearn.preprocessing import FunctionTransformer
invlognorm = FunctionTransformer(func, validate=True)
dfft = pd.DataFrame(invlognorm.fit_transform(amazonBooks_norm[['SalesRank']]), columns=['invlognorm_SalesRank'], index=amazonBooks.index)
dfft.head()
amazonBooks_norm = pd.concat([amazonBooks_norm, dfft], axis=1)
amazonBooks_norm = amazonBooks_norm.drop('SalesRank', axis=1)
amazonBooks_norm.head()

#Composite Score Calculation
scores=[]
for x in purchasedAsinNeighbors:
        scores.append((x,amazonBooks_norm.loc[x,'mms_AvgRating']*amazonBooks_norm.loc[x,'mms_DegreeCentrality']*amazonBooks_norm.loc[x,'mms_TotalReviews']*amazonBooks_norm.loc[x,'invlognorm_SalesRank']))

# Now I Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
BookAsinRecos=sorted(scores,key= itemgetter(1), reverse=True)
top5=[]

if len(BookAsinRecos)<5:
    for k in range(len(BookAsinRecos)):
        top5.append(BookAsinRecos[k][0])
else:
    for i in range(5):
        top5.append(BookAsinRecos[i][0])
print("\n")        
print("Top 5 Recommendations are:" )    
for y in top5:
    print({'Asin':y,'Title':amazonBooks.loc[y,'Title'], 'SalesRank':amazonBooks.loc[y,'SalesRank'], 'TotalReviews':amazonBooks.loc[y,'TotalReviews'], 'AvgRating':amazonBooks.loc[y,'AvgRating'], 'DegreeCentrality':amazonBooks.loc[y,'DegreeCentrality'],'ClusteringCoeff':amazonBooks.loc[y,'ClusteringCoeff']})
# The End
