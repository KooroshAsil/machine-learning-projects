import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
np.random.seed(42)

def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


def KMeans(dtframe, k, epsilon = 0.001):
    
    clusters = [[] for i in range(k)]
    centroids = []
        
    array_df = np.asarray(dtframe) # first we turn the dataframe into a numpy array
    n_points,n_features = array_df.shape # now using reshape to get the number of rows and columbs

    random_sample_indexes = np.random.choice(n_points,k, replace=False)

    centroids = [array_df[index] for index in random_sample_indexes]
        
    while True:
        clusters = make_clusters(centroids, k ,array_df) 
        old_centroids = centroids
        centroids = updata_centroids(clusters, k ,n_features, array_df)

        if finished(old_centroids, centroids, k, epsilon):
            break

    return cluster_labels(clusters, n_points)

def cluster_labels(clusters, n_points):
    labels = np.empty(n_points)
    for cluster_idx, cluster in enumerate(clusters):
        for sample_index in cluster:
            labels[sample_index] = cluster_idx
    return labels

def make_clusters(centroids, k, array_df):
    clusters = [[] for _ in range(k)]
    for index, sample in enumerate(array_df):
        centroid_index = closest_centroid(sample, centroids) 
        clusters[centroid_index].append(index) 
    return clusters

def closest_centroid(sample, centroids):
    distances = [euclidean_distance(sample, point) for point in centroids]
    closest_index = np.argmin(distances)
    return closest_index

def updata_centroids( clusters, k , n_features, array_df):
    centroids = np.zeros((k,n_features))
    for cluster_index, cluster in enumerate(clusters): # index of the cluster and self.cluster := [[1,6,3,...], [23,534, ... 13611]]
        cluster_mean = np.mean(array_df[cluster], axis=0)
        centroids[cluster_index] = cluster_mean
    return centroids

def finished(old_centroids, centroids, k, epsilon):
    # distances between each old and new centroids, fol all centroids
    distances = [
        euclidean_distance(old_centroids[i], centroids[i]) for i in range(k)
    ]
    return abs(sum(distances)) < epsilon

def plot_KMeans(file_load, result):
    X = file_load.iloc[:, :-1]
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=result, cmap='jet')
    plt.colorbar()
    plt.xlabel("PCA1")
    plt.ylabel("PCA2")
    plt.show()
    
df= pd.read_csv("Dry_Bean.csv")
dtframe = pd.DataFrame(df)
encoded_dtframe = pd.get_dummies(dtframe)
result = KMeans(encoded_dtframe, 5)
plot_KMeans(encoded_dtframe, result)