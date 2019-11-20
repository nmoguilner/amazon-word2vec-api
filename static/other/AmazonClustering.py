from sklearn.cluster import KMeans;
from sklearn.neighbors import KDTree;
import AmazonLoadModel
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from itertools import cycle

from wordcloud import WordCloud, ImageColorGenerator

# src: https://medium.com/ml2vec/using-word2vec-to-analyze-reddit-comments-28945d8cee57

def clustering_on_wordvecs(word_vectors, num_clusters):
    # Initalize a k-means object and use it to extract centroids
    kmeans_clustering = KMeans(n_clusters=num_clusters, init='k-means++');
    idx = kmeans_clustering.fit_predict(word_vectors);

    return kmeans_clustering.cluster_centers_, idx;


def get_top_words(index2word, k, centers, wordvecs):
    tree = KDTree(wordvecs);
    # Closest points for each Cluster center is used to query the closest 20 points to it.
    closest_points = [tree.query(np.reshape(x, (1, -1)), k=k) for x in centers];
    closest_words_idxs = [x[1] for x in closest_points];
    # Word Index is queried for each position in the above array, and added to a Dictionary.
    closest_words = {};
    for i in range(0, len(closest_words_idxs)):
        closest_words['Cluster #' + str(i)] = [index2word[j] for j in closest_words_idxs[i][0]]
    # A DataFrame is generated from the dictionary.
    df = pd.DataFrame(closest_words);
    df.index = df.index + 1
    return df;


def display_cloud(cluster_num, cmap):
    wc = WordCloud(background_color="black", max_words=100, max_font_size=60, colormap=cmap);
    wordcloud = wc.generate(' '.join(
        [AmazonLoadModel.asin_title_dict[word] for word in top_words['Cluster #' + str(cluster_num - 1).zfill(1)]]))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('data/WordClouds/cluster_' + str(cluster_num), bbox_inches='tight')


model = AmazonLoadModel.model
Z = model.wv.syn0;

centers, clusters = clustering_on_wordvecs(Z, 150);
centroid_map = dict(zip(model.wv.index2word, clusters));
top_words = get_top_words(model.wv.index2word, 500, centers, Z);

cmaps = cycle([
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])

for i in range(200):
    col = next(cmaps);
    display_cloud(i + 1, col)
