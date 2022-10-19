from array import array
from email.mime import image
import random
from re import X
import numpy as np
import klustr_utils

class KNN:
    def __init__(self,nDim):
        self.__nDim = nDim
        self.__image = None
        
    # 1 : Conversion png to ndarray
    def conversion_png_ndarray(self,dataImage):
        qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage)
        self.__image = arrayBinary
        
    # 2 : Utiliser les formules 
    def aireForme(self):
        return np.sum(np.count_nonzero(self.__image))
    
    def perimetreForme(self):
        return np.sum(self.__image[:,1:] != self.__image[:,:-1]) + np.sum(self.__image[1:,:] != self.__image[:-1,:])
    
    def centroideForme(self):
        c, r = np.meshgrid(np.arange(self.__image.shape[1]), np.arange(self.__image.shape[0]))
        return (np.sum(r * self.__image), np.sum(c * self.__image)) / self.aireForme(self.__image)

    # ContourForme pour 1 image
    def trouver_contour_forme_image(self):
        return self.aireForme() / self.perimetreForme() ** 2
    
    
    def trouverRatioForme(self):
        centroide = self.centroideForme()
        zeroPlusProche = np.abs(centroide - 0).argmin()
        
        
        

    
    def trouverSommeDistances(self):
        pass



    # Reshape le data en dimension Ndim
    def reshape_data(self):
        pass
        
        

        
    ## for i in liste_
        
    
    # 2 : On dispose l'objet à classifier
    # def perimetre():
    #     return 0
    
    # def formule1(self, width, height, perimetre):
    #     return (width * height) / pow(perimetre), 
        
    
    
    
    # 3 : Calculer la distance de l'objet par rapport à notre data
    
     
     
    # # 1- trouver le k (nombre de voisins)   
    
    # def randomize(self):
    #    self.__Matrix = np.random.randint(2,size=(self.__width, self.__height));
    #    print(self.__Matrix)
       
    # def convertir1D(self):
    #     self.__Matrix = self.__Matrix.flatten()
    #     print(self.__Matrix)
    
    # def trouverKVoisin(self):
    #     point = self.__Matrix[int(self.__width / 2), int(self.__height / 2)]
    #     self.__num_neighbor
        

    #     left = [self.__Matrix[int(self.__width / 2), int(self.__height / 2)-self.__distane]]
    #     right = [self.__Matrix[int(self.__width / 2), int(self.__height / 2)+self.__distane]]
    #     top = [self.__Matrix[int(self.__width / 2)-self.__distane, int(self.__height / 2)]]
    #     bottom = [self.__Matrix[int(self.__width / 2)+self.__distane, int(self.__height / 2)]]
       
    #     print(point)
    #     print(left)  
    #     print(right)
    #     print(top)
    #     print(bottom) 
    #     #sample = self.__Matrix[int(left):int(right),int(bottom):int(top)]
       
            
    
    # def trouverClasseFrquente():
    #     pass
        
    # def calculeDistance():
    #     pass
    
        
def main():
    knn_engine = KNN(3)
    

if __name__ == '__main__':
    main()
    

