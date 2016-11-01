# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:11 2015

@author: pablo
"""


import re
import math



class classifier:
    def __init__(self,getfeatures, filename = None):
   
       		# counts of feature/category combinations
    	self.fc={}
        # counts of document in each category
        self.cc = {}
        self.getfeatures = getfeatures
   
   # increase the count of a feature/category pair
    def incf(self, f, cat):
       self.fc.setdefault(f,{})
       self.fc[f].setdefault(cat,0)
       self.fc[f][cat]+=1
    
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat] += 1
       
   
   # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    
    # The number of items in a category
    def catcount(self,cat):
    	if cat in self.cc:
        	return float(self.cc[cat])
   		return 0.0
    
    #The total number of items
    def totalcount(self):
        return sum(self.cc.values())
        
    def categories(self):
        return self.cc.keys()
    
    def train(self,item,cat):
    	features = self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
        	self.incf(f,cat)
            
        self.incc(cat) 
        
    def fprob(self,f,cat):
        if self.catcount(cat)==0:
            return 0.0
        return self.fcount(f,cat)/self.catcount(cat)     
    
    def weightedprob(self, f, cat, prf, weight = 1.0, ap=0.5):
        # Calculate current probability
        basicprob = prf(f,cat)
         
        # Count the number of items the feature has appeared in all categories        
        totals = sum([self.fcount(f,c) for c in self.categories()])
        
        # Calculate the weighted average
        bp = (weight*ap+totals*basicprob)/(weight+totals)
        
        return bp
    
    def classify(self,item,default = None):
        probs = {}
        # Find the category with the highest probability
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item,cat)
            
            if probs[cat]>max:
                max = probs[cat]
                best = cat

        if probs[best]<0.1: return default
                
        # Make sure that the probability excedes threshold*next best
                
        for cat in probs:
            if cat==best: continue
            if probs[cat]*self.getthreshold(best)>probs[best]: return default
        
        return best
        
class naivebayes(classifier):
    
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds = {}
        
    def setthreshold(self,cat,t):
        self.thresholds[cat] = t
        
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]
    
    def docprob(self,item,cat):
        features = self.getfeatures(item)
        
        # Multiply the probabilities for all the features together
        p = 1.0
        for f in features: p*=self.weightedprob(f,cat,self.fprob)
        return p
    
    def prob(self,item,cat):
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item,cat)
        return docprob*catprob


def sampletrain(cl):
    cl.train('sport hokej soccer videohry','M')
    cl.train('boty fashion dieta kosmetika', 'F')
    
def getwords(url):
    splitter = re.compile('\W*')
    words = [s.lower() for s in splitter.split(url) if len(s)>2]
    return dict([(w,1) for w in words])
    
    
#@outputSchema('num:long')
#def predict(feature_vector):
#    cl = naivebayes(getwords)
#    sampletrain(cl)
# 
#    
#    return len(cl.classify(feature_vector,default='unknown'))    
    
if __name__ == '__main__':
    cl = naivebayes(getwords)    
#    cl.train('the quick brown fox jumps','good')
    
    
    sampletrain(cl)
    print cl.prob('pubcrawl.cz/en/prague-pub-crawl/','M')

    print cl.classify('pubcrawl.cz/en/prague-pub-crawl/',default = 'unknown')
    
