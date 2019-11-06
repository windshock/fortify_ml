# 참고 : https://lovit.github.io/nlp/machine%20learning/2018/03/21/kmeans_cluster_labeling/

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import math
import pandas as pd
import numpy as np
import os

base_dir = './data/'
excel_file = 'fortify_ml.xlsx'
test_file = 'test.xlsx'
excel_dir = os.path.join(base_dir,excel_file)
test_dir = os.path.join(base_dir,test_file)
df_from_excel=pd.read_excel(excel_dir,sheet_name='Sheet1',header=0,names=['Fortify_NodeType','k16','k18','k21','manual','vul?'],dtype={'Fortify_NodeType':str,'kmeans':str,'manual':str},na_values='NaN',thousands=',',comment='#')
df_from_test=pd.read_excel(test_dir,sheet_name='Sheet1',header=0,names=['Fortify_NodeType','k16','k18','k21','manual','vul?'],dtype={'Fortify_NodeType':str,'kmeans':str,'manual':str},na_values='NaN',thousands=',',comment='#')
docs = df_from_test.append(df_from_excel)['Fortify_NodeType'].values

k=math.ceil(len(docs)/2)

#find k
for i in range(k,0,-1):
    # vectorizing
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)

    # L2 normalizing
    X = normalize(X, norm='l2')

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