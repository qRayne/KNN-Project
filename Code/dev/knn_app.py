from array import array
from email.mime import image
from math import perm
from msilib.schema import Property
import random
from re import X
import re
import numpy as np
import klustr_utils


class KNN:
    def __init__(self,arrayMetrique,metriqueImageTest,nbVoisins,dimension,imageTest):
       self.__nbVoisins = nbVoisins
       self.__imageTest = self.conversion_png_ndarray(imageTest) # on converti l'image qu'on a 
       self.data_training = np.empty((0, dimension), dtype=np.float64) 
       self.__metriqueImageTest = metriqueImageTest
       self.__arrayMetrique = arrayMetrique
       
    
    @property
    def imageTest(self):
        return self.__imageTest
    
    @property
    def nbVoisins(self):
         return self.__nbVoisins
     
    @property
    def metriqueImageTest(self):
         return self.__metriqueImageTest
     
    @property
    def arrayMetrique(self):
         return self.__arrayMetrique

    # Conversion png to ndarray
    # prend en paramètre une image.png et la transforme de png->qimage et qimage ->ndarray
    def conversion_png_ndarray(self,dataImage):
        qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage)
        return arrayBinary

    def aireForme(self,dataImage):
        return np.sum(np.count_nonzero(dataImage))
    
    def perimetreForme(self,dataImage):
        # le deuxième data dans le tupe (-1, n ) ou n est le nombre de colonnes
        return np.sum(dataImage[:,1:] != dataImage[:,:-1]) + np.sum(dataImage[1:,:] != dataImage[:-1,:])

    def centroideForme(self,dataImage):
        c, r = np.meshgrid(np.arange(dataImage.shape[1]), np.arange(dataImage.shape[0]))
        return (np.sum(r * dataImage), np.sum(c * dataImage)) / self.aireForme(dataImage)

    #  on trouve le contour de l'image grâce à l'aire de l'image et son perimètre 
    def trouverContourFormeImage(self,dataImage):
        return self.aireForme(dataImage) / self.perimetreForme(dataImage) ** 2
    
    def trouverRatioImage(self,dataImage):
        pass
    
    def trouverNbSommets(self,dataImage):
        pass
        
    
        
def main():
    pass
    # carre = [[0,0,0,0,0,0,0,0,0,0],
    #                [0,0,0,0,0,0,0,0,0,0],
    #                [0,0,1,1,1,1,1,1,0,0],
    #                [0,0,1,1,1,1,1,1,0,0],
    #                [0,0,1,1,1,1,1,1,0,0],
    #                [0,0,1,1,1,1,1,1,0,0],
    #                [0,0,1,1,1,1,1,1,0,0],
    #                [0,0,1,1,1,1,1,1,0,0],
    #                [0,0,0,0,0,0,0,0,0,0],
    #                [0,0,0,0,0,0,0,0,0,0]]
    
    # carreNumpy = np.array(carre)
    # carreNumpy.flatten()
    # knn_engine = KNN(0,0,3,3,carreNumpy)



    # # ------------------------------------------ TEST CARRE   ---------------------------------------#    

    
    # print(f"Aire du carré : {knn_engine.aireForme(carreNumpy)}")
    # print(f"Permiètre du carré : {knn_engine.perimetreForme(carreNumpy)}")
    # print(f"Centroide du carré  : {knn_engine.centroideForme(carreNumpy)}")
    # print(f"Taille du tableau après l'ajout du carré  : {knn_engine.trouverContourFormeImage(carreNumpy)}")

if __name__ == '__main__':
    main()
    

