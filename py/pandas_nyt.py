import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer

data = pd.read_csv('nyt.csv')

data['keywords'] = data['keywords'].str.replace('[\W,]', ' ')
print(data.head(5))

hv = HashingVectorizer()

x = hv.fit_transform(data.keywords)

# --------------
# ----KMeans----
# --------------

# from sklearn.cluster import KMeans
# km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, verbose=opts.verbose)

# feedback stuff
# print("Clustering sparse data with %s" % km)
# t0 = time()
# km.fit(X)
# print("done in %0.3fs" % (time() - t0))
# print()

# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
# print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
# print("Adjusted Rand-Index: %.3f"
#       % metrics.adjusted_rand_score(labels, km.labels_))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, km.labels_, sample_size=1000))

# print()


# if not opts.use_hashing:
#     print("Top terms per cluster:")

#     if opts.n_components:
#         original_space_centroids = svd.inverse_transform(km.cluster_centers_)
#         order_centroids = original_space_centroids.argsort()[:, ::-1]
#     else:
#         order_centroids = km.cluster_centers_.argsort()[:, ::-1]

#     terms = vectorizer.get_feature_names()
#     for i in range(true_k):
#         print("Cluster %d:" % i, end='')
#         for ind in order_centroids[i, :10]:
#             print(' %s' % terms[ind], end='')
#         print()