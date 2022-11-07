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
    def __init__(self,dimension,image_test,nb_voisins=3):
       self.__nb_voisins = nb_voisins
       self.__image_test = self.conversion_png_ndarray(image_test) # on converti l'image qu'on a 
       self.__metrique_image_test = np.empty((0,dimension), dtype=np.float64) #[x,y,z]
       self.__liste_metriques_dataset = np.empty((0, dimension), dtype=np.float64) #[x,y,z], [x,y,z]
       self.__distance = 0
    
    @property
    def data_training(self):
        return self.__data_training
    
    @property
    def image_test(self):
        return self.__image_test
    
    @property
    def nb_voisins(self):
         return self.__nb_voisins
     
    @property
    def metrique_image_test(self):
         return self.__metrique_image_test
     
    @property
    def distance(self):
        return self.__distance
    
    @property
    def liste_metriques_dataset(self):
        return self.__liste_metriques_dataset
    
    def set_distance(self,distance):
        self.__distance = distance
        
    def set_liste_metriques_dataset(self,liste_metrique_dataset):
        self.__liste_metriques_dataset = liste_metrique_dataset
        
    def set_metrique_image_test(self,metrique_image_test):
        self.__metrique_image_test = metrique_image_test
        
    def set_nb_voisins(self,nb_voisins):
        self.__nb_voisins = nb_voisins
 
    # Conversion png to ndarray
    # prend en paramètre une image.png et la transforme de png->qimage et qimage ->ndarray
    def conversion_png_ndarray(self,dataImage):
        qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage)
        return arrayBinary

    def aire_forme(self,data_image):
        return np.sum(np.count_nonzero(data_image))
    
    def trouver_coordonnees_image(self,data_image):
        # on recupère en [x,y] chaque point qui contient 1 (soit un pixel qui est dessiner)
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
    
    def calcul_ratio_circularite(self,data_image):
        centroide = self.centroide_forme(data_image)
        arrayCoordonnes = self.trouver_coordonnees_image(data_image)
        # ici au lieu de faire une for loop afin de calculer chaque point sa distance
        # on calcule dans une matrice chaque point -> le calcul devient beaucoup plus rapide
        distancePoints = np.linalg.norm(arrayCoordonnes - centroide, axis=1)
        # retourne le ratio entre le cercleInscrit / cercleCirconscrit
        return (math.pi * (np.amin(distancePoints) **2)) /  (math.pi * (np.amax(distancePoints) **2))

    def calcul_ratio_distance_image(self,data_image):
        centroide = self.centroide_forme(data_image)
        arrayCoordonnes = self.trouver_coordonnees_image(data_image)
        # ici au lieu de faire une for loop afin de calculer chaque point sa distance
        # on calcule dans une matrice chaque point -> le calcul devient beaucoup plus rapide
        distancePoints = np.linalg.norm(arrayCoordonnes - centroide, axis=1)
        return np.amin(distancePoints) / np.amax(distancePoints)
            
    def calculer_distance_image_test_dataset(self,liste_metriques_dataset,metrique_image_test,nbVoisins):
        
        tableau_distance = np.empty(0)
        
        for data in liste_metriques_dataset:
            x_label = float(data[0]) - metrique_image_test[0,0] # x
            y_label = float(data[1]) - metrique_image_test[0,1] # y
            z_label = float(data[2]) - metrique_image_test[0,2] # z

            #ici on va calculer la distance à l'aide de la formule donnee
            distance = (math.pow(x_label,2) + math.pow(y_label,2) + math.pow(z_label,2)) ** 0.5
            tableau_distance = np.append(tableau_distance,distance)

        # # retourne 1,2 ou 3 distances selon le nbVoisins
        result = np.argpartition(tableau_distance,nbVoisins)
        return tableau_distance[result[:nbVoisins]]
    

