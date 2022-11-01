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
    def __init__(self,nb_voisins,dimension,image_test):
       self.__nb_voisins = nb_voisins
       self.__image_test = self.conversion_png_ndarray(image_test) # on converti l'image qu'on a 
       self.__data_training = np.empty((0, dimension), dtype=np.float64)  #[x,y,z, image], [x,y,z, image]
       self.__metrique_image_test = np.empty((0,dimension), dtype=np.float64) #[x,y,z]
       
       
    # ------------------------------------------ EXPLICATION ---------------------------------------#    
    # Lorsqu'on va creer un knn on va lui passer en paramètre la dimension, le nombre de voisins et l'image test
    # l'image test va être directement converti en png_ndarray
    # avec l'image on pourra calculer chacune des metrique qu'on mettra dans un tableau [x,y,z]
    # et ce tableau on l'ajoutera dans notre data_training avec un tag pour dire le nom de l'image et ses metriques
    # nos metriques sont : la 
       
       
    
    @property
    def data_training(self):
        return self.__data_training
    @property
    def image_test(self):
        return self.__imageTest
    
    @property
    def nb_voisins(self):
         return self.__nbVoisins
     
    @property
    def metrique_image_test(self):
         return self.__metriqueImageTest

    # Conversion png to ndarray
    # prend en paramètre une image.png et la transforme de png->qimage et qimage ->ndarray
    def conversion_png_ndarray(self,dataImage):
        qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage)
        return arrayBinary

    def aire_forme(self,data_image):
        return np.sum(np.count_nonzero(data_image))
    
    def perimetre_forme(self,data_image):
        # le deuxième data dans le tupe (-1, n ) ou n est le nombre de colonnes
        return np.sum(data_image[:,1:] != data_image[:,:-1]) + np.sum(data_image[1:,:] != data_image[:-1,:])

    def centroide_forme(self,data_image):
        c, r = np.meshgrid(np.arange(data_image.shape[1]), np.arange(data_image.shape[0]))
        return (np.sum(r * data_image), np.sum(c * data_image)) / self.aireForme(data_image)

    #  on trouve le contour de l'image grâce à l'aire de l'image et son perimètre 
    def calcul_complexite(self,data_image):
        return self.aireForme(data_image) / self.perimetre_forme(data_image) ** 2
    
    def calcul_ratio_image(self,data_image):
        pass
    
    def calcul_nb_sommets(self,data_image):
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
    

