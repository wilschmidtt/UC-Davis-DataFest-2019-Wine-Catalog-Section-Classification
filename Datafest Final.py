# DataFest - Wine Catalouge Section Detection using K-Means Algorithm

# Trying to Cluster DataFest words

from __future__ import print_function
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.cluster import KMeans 
import pyperclip
import numpy as np

pd.__version__

# Create Dataframe Object
color = pd.Series(['Red', 'White', 'Rose'])
type = pd.Series(['Still', 'Sparkling', 'Fortified'])

pd.DataFrame({ 'color': color, 'wine_type': type })

# Datafest wine Marks
PGHOST="datafest201912.library.ucdavis.edu"
PGDATABASE="postgres"
PGPORT="49152"
PGUSER="anon"
PGPASSWORD="anon"

conn_string = ("host={} port={} dbname={} user={} password={}") \
  .format(PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD)

conn=psycopg2.connect(conn_string)

# edit SQL string here
sql_command = "SELECT * FROM {}.{};".format("datafest", "mark")
marks = pd.read_sql(sql_command, conn)
marks.describe()

# All pages 
sql_command = "select page_id, p.page_ark from page p"
page = pd.read_sql(sql_command, conn)
page
row_idx = page.index[page['page_ark'] == "d7q36x-009"].tolist()
row_contents = page.iloc[row_idx]

# Save link to clipboard so you can paste into browser and view catalouge in question
page_link = 'https://datafest201912.library.ucdavis.edu'+row_contents['page_id'].values[0]
pyperclip.copy(page_link)

sql_command = "SELECT * FROM {} WHERE page_ark='{}';".format("rtesseract_words","d7q36x-009")
words = pd.read_sql(sql_command, conn)
words

# Creating the Dataset to use K-Means on
X = words.iloc[:, [2,3]].values

# Plotting the words based on bottom left point of word (NOTE: plot is reflected over x-axis. In the original data, the y-axis becomes positive in the downward direction)
plt.scatter(words['left'], words['top'])
ax = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.show()

# print(words.shape)

# Filter for words with confidence >80
height = words["bottom"] - words["top"] 
height = pd.DataFrame({"height" : height})
words  = words.join(height)
words= words.sort_values(by='height', ascending=False)
words = words[words["confidence"]>80]

# =============================================================================
### Use this block of code if you want to filter words by some height threshold
# large_words = words[words["height"] > 50 ]
# print(large_words.describe())
# print(large_words.shape)
# =============================================================================





# =============================================================================
# Start: Iteration 1
# =============================================================================


# Using the elbow method to find number of clusters 
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Using the max change in slope of elbow graph to find the ideal number of clusters
def slope(x1, y1, x2, y2): # do for each set of 2 points, do slope(n+1)-slope(n), and whichever is the greatest is the # of clusters
    m = (y2-y1)/(x2-x1)
    return m

slopes = []
for i in range(1, 10):
    slopes.append(slope(i, wcss[i-1], i+1, wcss[i]))

changes_in_slope = []
for i in range(len(slopes)-1):
    changes_in_slope.append(abs(slopes[i]-slopes[i+1]))

ideal_num_of_clusters = int(changes_in_slope.index(max(changes_in_slope))+2)

# Applying k-means to the dataset
kmeans = KMeans(n_clusters = ideal_num_of_clusters,  init='k-means++', max_iter=300, n_init=10, random_state=0)
y_kmeans = kmeans.fit_predict(X)
# Visualising the clusters 
for i in range(0, ideal_num_of_clusters):
    plt.scatter(X[y_kmeans==i, 0], X[y_kmeans==i, 1])
ax = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.title('Cluster of Words (iteration 1)')
plt.savefig('Cluster of Words - Iteration 1.png')
plt.show()


# =============================================================================
# End: Iteration 1
# =============================================================================





# =============================================================================
# Start: Iteration 2
# =============================================================================


# Puttig new clusters into their own dataframes
master_dataframes = {}
cluster_num = 1
new_dataframes = {}
for x in range(0, ideal_num_of_clusters):
    data = {'Col 1': X[y_kmeans==x, 0], 'Col 2': X[y_kmeans==x, 1]}
    new_dataframes["cluster_{0}".format(x+1)] = pd.DataFrame(data).to_numpy()

 
keys_new_dataframes = list(new_dataframes.keys())
for x in range(0, len(keys_new_dataframes)):
    X = new_dataframes[keys_new_dataframes[x]]
    # Elbow Method
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1,11), wcss)
    plt.title('The Elbow Method - Cluster {}'.format(x+1))
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    
    # Using the max change in slope of elbow graph to find the ideal number of clusters
    def slope(x1, y1, x2, y2): # do for each set of 2 points, do slope(n+1)-slope(n), and whichever is the greatest is the # of clusters
        m = (y2-y1)/(x2-x1)
        return m
    
    slopes = []
    for i in range(1, 10):
        slopes.append(slope(i, wcss[i-1], i+1, wcss[i]))
    
    changes_in_slope = []
    for i in range(len(slopes)-1):
        changes_in_slope.append(abs(slopes[i]-slopes[i+1]))
    
    ideal_num_of_clusters = int(changes_in_slope.index(max(changes_in_slope))+2)
    
    # Applying k-means to the dataset
    kmeans = KMeans(n_clusters = ideal_num_of_clusters,  init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(X)
   
    # Visualising the clusters 
    for i in range(0, ideal_num_of_clusters):
        plt.scatter(X[y_kmeans==i, 0], X[y_kmeans==i, 1])
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])    
    plt.title('Cluster of Words (cluster {} - iteration 2)'.format(x+1))
    plt.show()
    
    for s in range(0, ideal_num_of_clusters):
        data = {'Col 1': X[y_kmeans==s, 0], 'Col 2': X[y_kmeans==s, 1]}
        master_dataframes["cluster_{}".format(cluster_num)] = pd.DataFrame(data).to_numpy()
        cluster_num += 1
        
    
# =============================================================================
# End: Iteration 2         
# =============================================================================




# To plot each cluster separately and save to 
keys_master_dataframes = list(master_dataframes.keys())
for i in range(0, len(keys_master_dataframes)):
    plt.scatter(master_dataframes[keys_master_dataframes[i]][: , 0], master_dataframes[keys_master_dataframes[i]][: , 1])
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])    
    plt.title('Cluster {} - Iteration 2'.format(i+1))
    plt.savefig('Cluster {} - Iteration 2.png'.format(i+1))
    plt.show()
    
    
    
    
    
# =============================================================================
# Optional Iterations on Desired Cluster
# =============================================================================


desired_cluster = input("Enter cluster name (eg: cluster_2): ")
sub_dataframes = {}
while 'cluster_' not in desired_cluster:
    print('Please re-enter cluster name. Make sure syntax is correct.')
    desired_cluster = input("Enter cluster name (eg: cluster_2): ")
cluster_num = int(desired_cluster[-1])
X = master_dataframes[desired_cluster]
# Elbow Method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method - Cluster {}'.format(x+1))
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Using the max change in slope of elbow graph to find the ideal number of clusters
def slope(x1, y1, x2, y2): # do for each set of 2 points, do slope(n+1)-slope(n), and whichever is the greatest is the # of clusters
    m = (y2-y1)/(x2-x1)
    return m

slopes = []
for i in range(1, 10):
    slopes.append(slope(i, wcss[i-1], i+1, wcss[i]))

changes_in_slope = []
for i in range(len(slopes)-1):
    changes_in_slope.append(abs(slopes[i]-slopes[i+1]))

ideal_num_of_clusters = int(changes_in_slope.index(max(changes_in_slope))+2)

# Applying k-means to the dataset
kmeans = KMeans(n_clusters = ideal_num_of_clusters,  init='k-means++', max_iter=300, n_init=10, random_state=0)
y_kmeans = kmeans.fit_predict(X)
   
# Visualising the clusters 
for i in range(0, ideal_num_of_clusters):
    plt.scatter(X[y_kmeans==i, 0], X[y_kmeans==i, 1])
ax = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])    
plt.title('Cluster of Words (Cluster {} - Iteration 3)'.format(cluster_num))
plt.savefig('Cluster {} - Iteration 3.png'.format(cluster_num))
plt.show()

for s in range(0, ideal_num_of_clusters):
        data = {'Col 1': X[y_kmeans==s, 0], 'Col 2': X[y_kmeans==s, 1]}
        sub_dataframes["cluster_{}".format(s+1)] = pd.DataFrame(data).to_numpy()
        
keys_sub_dataframes = list(sub_dataframes.keys())
for i in range(0, len(keys_sub_dataframes)):
    plt.scatter(sub_dataframes[keys_sub_dataframes[i]][: , 0], sub_dataframes[keys_sub_dataframes[i]][: , 1])
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])    
    plt.title('Cluster {} Interation 3: Sub-Cluster {}'.format(cluster_num, i+1))
    plt.savefig('Cluster {} Iteration 3, Sub Cluster {}.png'.format(cluster_num, i+1))
    plt.show()