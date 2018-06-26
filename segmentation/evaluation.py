import time
import pandas as pd
from kmodes.kmodes import KModes
from sklearn.metrics import silhouette_score, silhouette_samples
from segmentation.helpers.JsonProcessor import JsonProcessor
from segmentation.helpers import urlKeywordExtractor as urlExtract

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/largeFileAfterPP.json'
droppedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/droppedDF.csv'
droppedPCM = '/Users/george/droppedDFPCM.csv'
otherPCM = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/20juneSmallPCM.csv'

# This messy part of code is a sandbox, currently holding the code
# to calculate and plot silhouette graphs for a range of K.

data_frame = jsonTools.read_and_sort_data(filePath)
data_frame = jsonTools.pre_process(data_frame)

#data_frame = data_frame.drop(['transactionPath'], axis=1)
#data_frame = data_frame.astype(str)
#data_frame = pd.read_csv(droppedData)

range_n_clusters = range(28, 29)
# a is the pre-computed matrix using the gower coefficient, using the daisy function in R.
a = pd.read_csv(otherPCM)

for n_clusters in range_n_clusters:

    fig, (ax1) = plt.subplots(1, 1)
    fig.set_size_inches(18, 10)

    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(data_frame) + (n_clusters + 1) * 10])
    kmodes_cao = KModes(n_clusters=n_clusters, init='Cao', verbose=0)
    kmodes_cao.fit_predict(data_frame)

    column_names = list(data_frame.columns.values)
    clusters = pd.DataFrame(kmodes_cao.cluster_centroids_, columns=column_names)

    b = kmodes_cao.labels_
    silhouette_avg = silhouette_score(a, b, metric='precomputed')

    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    sample_silhouette_values = silhouette_samples(a, b, metric='precomputed')

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[b == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title(("Silhouette analysis for KModes clustering "
                  "with clusters = %d" % n_clusters))
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # Draw white circles at cluster centers

    plt.show()

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", to_json=False)
