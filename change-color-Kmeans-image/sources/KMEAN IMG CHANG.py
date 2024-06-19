from sklearn.cluster import KMeans
import numpy
import matplotlib.pyplot as mpl

img = mpl.imread('b1.jpg')
w = img.shape[0]
h = img.shape[1]
img = img.reshape(h * w, 3)
kmean = KMeans(n_clusters=3).fit(img)
labels = kmean.predict(img)
clusters = kmean.cluster_centers_
img2 = numpy.zeros_like(img)

for i in range(len(img2)):
     img2[i] = clusters[labels[i]]

img2 = img2.reshape(w, h, 3)
mpl.imshow(img2)
mpl.show()