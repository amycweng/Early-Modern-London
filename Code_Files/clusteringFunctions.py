'''
Unsupervised k-means clustering on plain text file versions of EEBO-TCP texts. 

Produces a user-specified number of clusters based on term frequency vectorization. 
These clusters are described using the keywords found in their corresponding entries 
in a metadata CSV file made using metadata.py in Stage I. 

The vectorize and cluster functions are adapted from the EarlyPrint Lab: 
    https://earlyprint.org/jupyterbook/unsupervised.html
The topTerms function is adapted from 
    https://pythonprogramminglanguage.com/kmeans-text-clustering/ 
The elbow and intercluster functions are adapted from Yellowbrick's documentation: 
    https://www.scikit-yb.org/en/latest/index.html
'''
import os
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def elbow(df):
    from yellowbrick.cluster.elbow import kelbow_visualizer
    kelbow_visualizer(KMeans(), df, k=(2, 10),timings=False)
    # kelbow_visualizer(KMeans(), df, k=(2, 10),metric='calinski_harabasz',timings=False)
    # kelbow_visualizer(KMeans(), df, k=(2, 10),metric='silhouette',timings=False)
    
def intercluster(model,num):
    from yellowbrick.cluster import intercluster_distance
    intercluster_distance(KMeans(num),model, embedding='mds') 

def pca_cluster(df,num, tcpIDs,idToTitle,toPrint):
    pca = PCA(n_components=2)
    pca_results = pca.fit_transform(df) 
    model = KMeans(n_clusters=num) 
    label = model.fit_predict(pca_results) 
    kmeans_groups = defaultdict(list)
    for k,v in zip(label,tcpIDs):
        kmeans_groups[k].append(v)

    u_labels = np.unique(label)
    groupColors = {0:'pink',1:'purple',2:'darkblue',3:'plum',4:'palevioletred',5:'darkgreen'}
    for i in u_labels:
        plt.scatter(pca_results[label == i , 0] , pca_results[label == i , 1] , label = i,color=groupColors[i])
    plt.legend()
    plt.figure(figsize=(20,10))
    plt.show()

    return kmeans_groups