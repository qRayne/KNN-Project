import random
import numpy as np

class KNN:
    def __init__(self, width, height, distance):
        self.__width = width
        self.__height = height
        self.__Matrix = []
        self.__distane = 1
        self.__num_neighbor = 0
        self.randomize()
        #self.convertir1D()
     
     
    # 1- trouver le k (nombre de voisins)   
    
    def randomize(self):
       self.__Matrix = np.random.randint(2,size=(self.__width, self.__height));
       print(self.__Matrix)
       
    def convertir1D(self):
        self.__Matrix = self.__Matrix.flatten()
        print(self.__Matrix)
    
    def trouverKVoisin(self):
        point = self.__Matrix[int(self.__width / 2), int(self.__height / 2)]
        self.__num_neighbor
        
        
        left = [self.__Matrix[int(self.__width / 2), int(self.__height / 2)-self.__distane]]
        right = [self.__Matrix[int(self.__width / 2), int(self.__height / 2)+self.__distane]]
        top = [self.__Matrix[int(self.__width / 2)-self.__distane, int(self.__height / 2)]]
        bottom = [self.__Matrix[int(self.__width / 2)+self.__distane, int(self.__height / 2)]]
       
        print(point)
        print(left)  
        print(right)
        print(top)
        print(bottom) 
        #sample = self.__Matrix[int(left):int(right),int(bottom):int(top)]
       
            
    
    def trouverClasseFrquente():
        pass
        
    def calculeDistance():
        pass
    
        
def main():
    knn_algo = KNN(10, 10, 10)
    
    knn_algo.trouverKVoisin()
    
    
    
   

   

if __name__ == '__main__':
    main()
    

