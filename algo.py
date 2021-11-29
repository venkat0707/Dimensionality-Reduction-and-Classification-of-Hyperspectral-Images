import sys
import os
import numpy as np
from tqdm import tqdm
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from load import PCA
import matplotlib.pyplot as plt
from scipy.io import loadmat,whosmat
image_fullpath=sys.argv[1]
image_name=sys.argv[2]
data=loadmat(str(image_fullpath))
b=whosmat(str(image_fullpath))
a=b[0]            
j=a[0]        
X=data[j] 
if(j[0]=="p"):y=loadmat("media/PaviaU_gt.mat")['paviaU_gt']
elif(j[0]=="i"):y=loadmat("media/Indian_pines_gt.mat")['indian_pines_gt']
elif(j[0]=="s"):y=loadmat("media/Salinas_gt.mat")['salinas_gt']
else:print("not found")
s1=y.shape[0]
s2=y.shape[1]

plt.figure(figsize=(10,10))
plt.imshow(X[:,:,56])
plt.axis('off')
plt.title('color')
plt.savefig('media/image.jpg')


X=X.reshape(-1,X.shape[2])
new=X
new_y=y.ravel()

#empty array
B = np.empty((X.shape[0],X.shape[1]), int)

#logic for replace 0's with 1000 in pavia dataset

for i in range(0, X.shape[0]):
    for j in range(0,X.shape[1]):
        if(X[i][j]==0):X[i][j]=-1
        if(new_y[i]!=0):B[i][j]=X[i][j]
        
        
        
a=B[np.nonzero(B)]
a=a.reshape(-1,X.shape[1])




for i in range(0, a.shape[0]):
    for j in range(0,a.shape[1]):
        if(a[i][j]==-1):a[i][j]=0
        
        
#removing 0's in groundtruth dataset
y=new_y[np.nonzero(new_y)]



#PCA for Dimensionality Reduction
pca = PCA(10)
pca.fit(a)
principle_components= pca.transform(a)


#Training Data Using PCA
X_train, X_test, y_train, y_test, indices_train, indices_test  = train_test_split(principle_components, y,  range(a.shape[0]),test_size = 0.30, random_state =13)
svm = SVC(kernel='rbf',degree = 10, gamma='scale', cache_size=1024*7)
svm.fit(X_train, y_train)
#PCA for Calssification
pca = PCA(10)
pca.fit(new)
new= pca.transform(new)
#Testing Data on Classification
X_train, X_test, y_train, y_test, indices_train, indices_test  = train_test_split(new,new_y,range(new.shape[0]),test_size = 0.30, random_state =13)
y_pred = svm.predict(X_test)
pre = y_pred
clmap = [0]*X.shape[0]
for i in tqdm(range(len(indices_train))):
    clmap[indices_train[i]] = new_y[indices_train[i]]
for i in tqdm(range(len(indices_test))):
    clmap[indices_test[i]] = pre[i]
    
    
    
#Classification Image   
plt.figure(figsize=(10,10))
plt.imshow(np.array(clmap).reshape(s1,s2), cmap='jet')
plt.colorbar()
plt.axis('off')
plt.title('Classification Map')
plt.savefig( 'media/Classification_map.jpg')


#Groundtruth Image
plt.figure(figsize=(10,10))
plt.imshow(new_y.reshape(s1,s2), cmap='jet')
plt.colorbar()
plt.axis('off')
plt.title('Ground Truth')
plt.savefig('media/ground_truth.jpg')



                



