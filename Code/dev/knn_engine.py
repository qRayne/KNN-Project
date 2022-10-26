from array import array
from email.mime import image
import random
from re import X
import numpy as np
import klustr_utils
class KNN:
    def __init__(self):
        self.__arrayImages = np.array([])
        self.__x = np.array([])
        self.__y = np.array([])
        self.__z= np.array([])
        self.__arrayDescripteur = np.array([]) # self.__x,self.__y,self.__z [x,y,z] pour chaque image
        
        
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
                
                

        
    # 1 : Conversion png to ndarray
    def conversion_png_ndarray(self,dataImage):
        #qImage = klustr_utils.qimage_argb32_from_png_decoding(dataImage)
        #arrayBinary = klustr_utils.ndarray_from_qimage_argb32(qImage)
        #test 
        arrayBinary = dataImage
        self.__arrayImages = np.append(self.__arrayImages,arrayBinary)
        
               
    # 2 : Utiliser les formules

    def aireForme(self,imageBinary):
        return np.sum(np.count_nonzero(imageBinary))
    
    def perimetreForme(self,imageBinary):
        imageBinary2d = np.reshape(imageBinary, (-1, 2))
        return np.sum(imageBinary2d[:,1:] != imageBinary2d[:,:-1]) + np.sum(imageBinary2d[1:,:] != imageBinary2d[:-1,:])
    
    def centroideForme(self,imageBinary):
        # imageBinary2d = np.reshape(imageBinary, (-1, 2))
        # c, r = np.meshgrid(np.arange(imageBinary2d.shape[1]), np.arange(imageBinary2d.shape[0]))
        # return (np.sum(r * imageBinary2d), np.sum(c * imageBinary2d)) / self.aireForme(imageBinary2d)
        pass

    
    def trouverContourFormeImage(self):
        for imageBinary in self.__arrayImages:
            print(imageBinary)
            #self.__x  = np.append(self.__x,self.aireForme(imageBinary) / self.perimetreForme(imageBinary) ** 2)
            
    # def trouverRatioImage(self):
    #     #for imageBinary in self.__arrayImages:
    #     pass
            
              
        
    
    # def centroideForme(self):
    #     c, r = np.meshgrid(np.arange(self.__image.shape[1]), np.arange(self.__image.shape[0]))
    #     return (np.sum(r * self.__image), np.sum(c * self.__image)) / self.aireForme(self.__image)

    # # ContourForme pour 1 image
    # def trouverContourFormeImage(self):
    #     for imageBinary in self.__arrayImages:
    #         np.append(self.__x,np.sum(np.count_nonzero(imageBinary)))
            
    
    #     return self.aireForme() / self.perimetreForme() ** 2
    
    
    # def trouverRatioForme(self):
    #     centroide = self.centroideForme()
    #     zeroPlusProche = np.abs(centroide).argmin()
    #     zeroPlusLoin = np.abs()
        
        
        

    
    # def trouverSommeDistances(self):
    #     pass



    # # Reshape le data en dimension Ndim
    # def reshapeData(self):
    #     pass
        
        

        
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
    knn_engine = KNN()
    matrice = knn_engine.init_matrice()
    matrice2 = knn_engine.init_matrice()

    knn_engine.conversion_png_ndarray(matrice)
    knn_engine.conversion_png_ndarray(matrice2)
    
    
    print(matrice)
    #knn_engine.aireForme
    
    print('Aire: ' + str(knn_engine.aireForme(matrice)))
    #print('Centroide: ' + str(knn_engine.centroideForme(matrice)))
    #print('Perimetre: ' + str(knn_engine.perimetreForme(matrice)))
    knn_engine.trouverContourFormeImage()
    

if __name__ == '__main__':
    main()
    

