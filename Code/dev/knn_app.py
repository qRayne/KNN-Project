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
    def __init__(self):
        self.__x = np.array([])
        self.__y = np.array([])
        self.__z= np.array([])
        
        
        
    # ------------------------------------------ TEST MATRICE   ---------------------------------------#    

    def init_matrice(self):
        matrice = [[0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0]]
        matriceNumpy = np.array(matrice)
        return matriceNumpy.flatten()
    
    def init_matrice2(self):
        matrice = [[0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,1,1,0,0,0,0],
                   [0,0,0,1,1,1,1,1,0,0],
                   [0,0,1,1,1,1,1,1,0,0],
                   [0,1,1,1,1,1,1,1,1,0],
                   [1,1,1,1,1,1,1,1,1,1],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0,0,0]]
        matriceNumpy = np.array(matrice)
        return matriceNumpy.flatten()
        
        
    # Conversion png to ndarray
    # prend en paramètre une image.png et la transforme de png->qimage et qimage ->ndarray
    def conversion_png_ndarray(self,dataImage):
        qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage) 
        return arrayBinary

    def aireForme(self,imageBinary):
        return np.sum(np.count_nonzero(imageBinary))
    
    def perimetreForme(self,imageBinary):
        # le deuxième data dans le tupe (-1, n ) ou n est le nombre de colonnes
        imageBinary2d = np.reshape(imageBinary,(-1,10))
        return np.sum(imageBinary2d[:,1:] != imageBinary2d[:,:-1]) + np.sum(imageBinary2d[1:,:] != imageBinary2d[:-1,:])

    def centroideForme(self,imageBinary):
        imageBinary2d = np.reshape(imageBinary,(-1,10))
        c, r = np.meshgrid(np.arange(imageBinary2d.shape[1]), np.arange(imageBinary2d.shape[0]))
        return (np.sum(r * imageBinary2d), np.sum(c * imageBinary2d)) / self.aireForme(imageBinary2d)

    #  on trouve le contour de l'image grâce à l'aire de l'image et son perimètre 
    def trouverContourFormeImage(self,imageBinary):
        try:
            self.__x  = np.append(self.__x,self.aireForme(imageBinary) / self.perimetreForme(imageBinary) ** 2)
        except:
            print("le contour n'a pas pu être calculer")
        finally:
            print("le contour a été ajouter")
            return self.__x.size
        
    
        
def main():
    knn_engine = KNN()
    carre = knn_engine.init_matrice()
    triangle = knn_engine.init_matrice2()



    # ------------------------------------------ TEST CARRE   ---------------------------------------#    

    
    print(f"Aire du carré : {knn_engine.aireForme(carre)}")
    print(f"Permiètre du carré : {knn_engine.perimetreForme(carre)}")
    print(f"Centroide du carré  : {knn_engine.centroideForme(carre)}")
    print(f"Taille du tableau après l'ajout du carré  : {knn_engine.trouverContourFormeImage(carre)}")

    
    # ------------------------------------------ TEST TRIANGLE   ---------------------------------------#    

    print(f"Aire du triangle : {knn_engine.aireForme(triangle)}")
    print(f"Permiètre du triangle : {knn_engine.perimetreForme(triangle)}")
    print(f"Centroide du triangle : {knn_engine.centroideForme(triangle)}")
    print(f"Taille du tableau après l'ajout du triangle  : {knn_engine.trouverContourFormeImage(triangle)}")
    
    
    
    



if __name__ == '__main__':
    main()
    

