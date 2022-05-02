import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from scipy import linalg as la
class IPCA():

    #initialization
    def __init__(self, n_components):
        self.n_components = n_components
        self.iteration = 0
        
        
        
        
        
        

    def fit(self, X):
        
        n_samples, n_features = X.shape 
        # initially
        if self.iteration == 0:  
            self.mean_ = np.zeros([n_features], float)
            self.components_ = np.zeros([self.n_components,n_features], float)
      
        # incrementally fit the model
        for i in range(0,X.shape[0]):
            self.partial_fit(X[i,:])
        
        # update explained_variance_ratio_
        self.explained_variance_ratio_ = np.sqrt(np.sum(self.components_**2,axis=1))
        
        # sort by explained_variance_ratio_
        idx = np.argsort(-self.explained_variance_ratio_)
        self.explained_variance_ratio_ = self.explained_variance_ratio_[idx]
        self.components_ = self.components_[idx,:]
        
        return self
        
        
        
        
        
       #fit the model partially
    def partial_fit(self, u):
       
        n = float(self.iteration)
        V = self.components_
        w1 = float(n+2-1)/float(n+2)    
        w2 = float(1)/float(n+2) 
        # update mean
        self.mean_ = w1*self.mean_ + w2*u
        # mean center u        
        u = u - self.mean_
        # update components
        for j in range(0,self.n_components):
            
            if j > n:
                # the component has already been init to a zerovec
                pass
            
            elif j == n:
                # set the component to u 
                V[j,:] = u
            else:       
                # update the components
                V[j,:] = w1*V[j,:] + w2*np.dot(u,V[j,:])*u / la.norm(V[j,:])
                
                normedV = V[j,:] / la.norm(V[j,:])
            
                u = u - np.dot(np.dot(u.T,normedV),normedV)
        
       
        self.iteration += 1
        self.components_ = V
        return
    
    
    #transform the data into the hyper-plane
    def transform(self, X):
       
     
        X_transformed = X - self.mean_
     
        return np.dot(X_transformed, self.components_.T)

  
