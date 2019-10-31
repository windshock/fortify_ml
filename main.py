# 참고 : https://lovit.github.io/nlp/machine%20learning/2018/03/21/kmeans_cluster_labeling/

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import math
import pandas as pd
import os

base_dir = './data/'
excel_file = 'fortify_ml2.xlsx'
excel_dir = os.path.join(base_dir,excel_file)
df_from_excel=pd.read_excel(excel_dir,sheet_name='Sheet1',header=0,names=['Fortify_NodeType','k16','k18','k21','manual','vul?'],dtype={'Fortify_NodeType':str,'kmeans':str,'manual':str},na_values='NaN',thousands=',',comment='#')
docs = df_from_excel['Fortify_NodeType'].values
k=math.ceil(len(docs)*0.34615)

# vectorizing
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)

# L2 normalizing
X = normalize(X, norm='l2')

# training k-means
kmeans = KMeans(n_clusters=k).fit(X)

# trained labels and cluster centers
labels = kmeans.labels_
centers = kmeans.cluster_centers_

print(labels)
print(math.ceil((len(docs)*0.4)))