import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier

from ml_algorithms.haara_recognition import MAX_DISTANCE

clf = KNeighborsClassifier(3, algorithm='brute')


def predict(embedding):
    return clf.predict(embedding)


# MAX_DISTANCE - 0.10000000001
def clustering(embeddings):
    db = DBSCAN(eps=MAX_DISTANCE - 0.2, min_samples=2, metric='euclidean', algorithm='brute').fit(embeddings)

    # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # core_samples_mask[db.core_sample_indices_] = True

    # # Number of clusters in labels, ignoring noise if present.
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # n_noise_ = list(labels).count(-1)

    # for label, name in zip(db.labels_, images_names):
    #     print(label, name)

    return db.components_, db.labels_


def fit(components, labels):
    clf.fit(components, labels)
    return
