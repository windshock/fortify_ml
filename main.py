# 참고 : https://lovit.github.io/nlp/machine%20learning/2018/03/21/kmeans_cluster_labeling/

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import math
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from sklearn.metrics import silhouette_score
import seaborn as sns


base_dir = './data/'
excel_file = 'fortify_ml.xlsx'
test_file = 'test.xlsx'
excel_dir = os.path.join(base_dir,excel_file)
test_dir = os.path.join(base_dir,test_file)
df_from_excel=pd.read_excel(excel_dir,sheet_name='Sheet1',header=0,names=['Fortify_NodeType','k16','k18','k21','manual','vul?'],dtype={'Fortify_NodeType':str,'kmeans':str,'manual':str},na_values='NaN',thousands=',',comment='#')
df_from_test=pd.read_excel(test_dir,sheet_name='Sheet1',header=0,names=['Fortify_NodeType','k16','k18','k21','manual','vul?'],dtype={'Fortify_NodeType':str,'kmeans':str,'manual':str},na_values='NaN',thousands=',',comment='#')
docs = df_from_test.append(df_from_excel)['Fortify_NodeType'].values

k=math.ceil(len(docs)/2)
"""
# 최적의 k 값을 통계적으로 분석하기.. elbow curve 기울기 값이 1이하, Silhouette Coefficient 1과 가까운 수
# 사전지식으로 최적의 k 값을 찾는 것보다 더 많은 군집을 요구하는 듯.
distorsions = []

for i in range(2,k):
    kmeans = KMeans(n_clusters=i)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)
    X = normalize(X, norm='l2')
    kmeans = KMeans(n_clusters=i).fit(X)
    sil_coeff = silhouette_score(X,kmeans.labels_,metric='euclidean')
    print("For n_clusters={}, The Silhouette Coefficient is {}".format(i, sil_coeff))

    distorsions.append(kmeans.inertia_)

fig = plt.figure()
plt.plot(range(2,k),distorsions,marker='o')
plt.grid(True)
plt.ylabel('Distortion')
plt.xlabel('k')
plt.title('Elbow curve')
plt.show()
"""

# vectorizing
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)
df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
#reduced_data = X.toarray()

# L2 normalizing
X = normalize(X, norm='l2')

#find k
for i in range(k,0,-1):


    # training k-means
    kmeans = KMeans(n_clusters=i).fit(X)

    # check test data
    # 사람의 의도와 다르게 기계가 같다고 구분한 데이터
    if (kmeans.labels_[2] == kmeans.labels_[3]):
        k=i+1
        kmeans = KMeans(n_clusters=k).fit(X)
        break
    # 사람의 분류가 잘못 되었던 데이터
    if (kmeans.labels_[0] == kmeans.labels_[1]):
        k=i
        break

if k == math.ceil(len(docs)*0.5):
    print("this is fail!!!")

# trained labels and cluster centers
labels = kmeans.labels_
centers = kmeans.cluster_centers_

print(labels)
print("k is ", k)

#그래프 그리다 실패 어찌 그리나?
"""
#df = pd.DataFrame(X)
#df['category'] = labels
#sns.lmplot('x','y',data=df,fit_reg=False,scatter_kws={"s":200},hue="category")
#plt.matshow(df.corr())
#plt.xticks(range(len(df.columns)), df.columns)
#plt.yticks(range(len(df.columns)), df.columns)
#y_kmeans = kmeans.predict(X)
#plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
#centers = kmeans.cluster_centers_
#plt.scatter(centers[:, ], c='black', s=200, alpha=0.5);
#plt.show()

for i in range(k):
    # select only data observations with cluster label == i
    ds = X[np.where(labels==i)]
    # plot the data observations
    print("a")
    plt.plot(ds[:,0],ds[:,1],'o')
    # plot the centroids
    lines = plt.plot(centers[i,0],centers[i,1],'kx')
    # make the centroid x's bigger
    plt.setp(lines,ms=15.0)
    plt.setp(lines,mew=2.0)
plt.show()
"""