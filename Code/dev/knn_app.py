from array import array
from dis import dis
from email.mime import image
from math import perm
from msilib.schema import Property
import random
from re import X
import re
import numpy as np
import klustr_utils
import math


class KNN:
    #  def __init__(self,nb_voisins,dimension,image_test):
    def __init__(self,nb_voisins,dimension,image_test):
       self.__nb_voisins = nb_voisins
       self.__image_test = image_test
       #self.__image_test = self.conversion_png_ndarray(image_test) # on converti l'image qu'on a 
       self.__data_training = np.empty((0, dimension), dtype=np.float64)  #[x,y,z, image], [x,y,z, image]
       self.__metrique_image_test = np.empty((0,dimension), dtype=np.float64) #[x,y,z]
    
    @property
    def data_training(self):
        return self.__data_training
    
    @property
    def image_test(self):
        return self.image_test
    
    @property
    def nb_voisins(self):
         return self.nb_voisins
     
    @property
    def metrique_image_test(self):
         return self.__metrique_image_test

    # Conversion png to ndarray
    # prend en paramètre une image.png et la transforme de png->qimage et qimage ->ndarray
    def conversion_png_ndarray(self,dataImage):
        qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage)
        return arrayBinary

    def aire_forme(self,data_image):
        return np.sum(np.count_nonzero(data_image))
    
    def trouver_coordonnees_image(self,data_image):
        return np.argwhere(data_image == 1)
    
    def perimetre_forme(self,data_image):
        # le deuxième data dans le tupe (-1, n ) ou n est le nombre de colonnes
        return np.sum(data_image[:,1:] != data_image[:,:-1]) + np.sum(data_image[1:,:] != data_image[:-1,:])

    def centroide_forme(self,data_image):
        c, r = np.meshgrid(np.arange(data_image.shape[1]), np.arange(data_image.shape[0]))
        return ((np.sum(r * data_image)), np.sum(c * data_image)) / self.aire_forme(data_image)

    #  on trouve la complexite de l'image grâce à l'aire de l'image et son perimètre
    #  notre unité de mesure sera le ratio qui lui sera présent pour chacune des formes
    def calcul_complexite(self,data_image):
        return 1 - ((4 * math.pi) * self.aire_forme(data_image) / self.perimetre_forme(data_image) ** 2)
    
    def calcul_ratio_image(self,data_image):
        centroide = self.centroide_forme(data_image)
        arrayCoordonnes = self.trouver_coordonnees_image(data_image)
        distancePoints = []
        
        for point in arrayCoordonnes:
            distancePoints.append(np.linalg.norm(centroide - point))
        
        distancePointsEnNumpy = np.array(distancePoints)
        # retourne le ratio entre le cercleInscrit / cercleCirconscrit
        return (math.pi * (np.amin(distancePointsEnNumpy) **2)) /  (math.pi * (np.amax(distancePointsEnNumpy) **2))
        
    
    def calcul_ratio_distance_image(self,data_image):
        centroide = self.centroide_forme(data_image)
        arrayCoordonnes = self.trouver_coordonnees_image(data_image)
        distancePoints = []
        
        for point in arrayCoordonnes:
            distancePoints.append(np.linalg.norm(centroide - point))
        
        distancePointsEnNumpy = np.array(distancePoints)
        # retourne le ratio entre la distance min / distance max
        return np.amin(distancePointsEnNumpy) / np.amax(distancePointsEnNumpy)     
    
        
def main():
    carre =        [[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]]
    
    carreNumpy = np.array(carre)
    carreNumpy.flatten()
    
    knn_engine = KNN(3,3,carreNumpy)
    
    print (f" aire du carré : {knn_engine.aire_forme(carreNumpy)}")
    print (f" permietre du carré : {knn_engine.perimetre_forme(carreNumpy)}")
    print (f" centroide du carré : {knn_engine.centroide_forme(carreNumpy)}")
    print (f" complexité du carré : {knn_engine.calcul_complexite(carreNumpy)}")
    print (f" ratio de circularité du carré : {knn_engine.calcul_ratio_image(carreNumpy)}")
    print (f" ratio de distance du carré : {knn_engine.calcul_ratio_distance_image(carreNumpy)}")


if __name__ == '__main__':
    main()
    

