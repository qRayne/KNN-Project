from multiprocessing import connection
from sqlite3 import connect
import sys

import numpy as np
from klustr_dao import *
from knn_app import KNN
from db_credential import PostgreSQLCredential

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout


import psycopg2

class MyData:
    
    def __init__(self, size=100):
        self.__rng = np.random.default_rng()
        self.__data = np.zeros((3, size), np.float32)

    @property
    def data(self):
        return self.__data
    
    def randomize_uniform(self, min=0., max=1.):
        self.__data[:] = self.__rng.uniform(min, max, self.__data.shape)

    def randomize_normal(self, mean=0., std=1.):
        self.__data[:] = self.__rng.normal(mean, std, self.__data.shape)


class ScatterDiagram:
    
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2
        
        self.__figure = plt.figure(figsize=(5, 5))
        axes = plt.axes( projection='3d')
        axes.set_xlabel('Ratio Complexite', fontweight='bold')
        axes.set_ylabel('Ratio Circularite', fontweight='bold')
        axes.set_zlabel('Ratio Distance', fontweight='bold')
        axes.set_title("Graphique de dispersion")

        self.__source1 = axes.scatter3D(self.__data1.data[0,:], self.__data1.data[1,:], self.__data1.data[2,:], color='blue', marker="o")
        self.__source2 = axes.scatter3D(self.__data2.data[0,:], self.__data2.data[1,:], self.__data2.data[2,:], color='magenta', marker="*")

        self.__canvas = FigureCanvas(self.__figure)
        self.__canvas.draw()
        
    def update_data(self):
        self.__source1._offsets3d = (self.__data1.data[0,:], self.__data1.data[1,:], self.__data1.data[2,:])
        self.__source2._offsets3d = (self.__data2.data[0,:], self.__data2.data[1,:], self.__data2.data[2,:])
        plt.draw()

    @property        
    def widget(self):
        return self.__canvas
    
    def set_data1(self,data):
        self.__data1 = data
        
    def set_data2(self,data2):
        self.__data2 = data2
    
    
class myApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ---------------------------- (Dataset) - Global menu--------------------------------#
        self.__group_data_set = QtWidgets.QGroupBox('Dataset')
        
        # Dataset - list deroulante
        self.__menu_list_data_layout = QVBoxLayout()
        self.__menu_data_list = QtWidgets.QComboBox()
        self.__menu_list_data_layout.addWidget(self.__menu_data_list)
        
        ############## Dataset - included in dataset ####################
        self.__included_in_dataset_box = QtWidgets.QGroupBox('Included in dataset')
        self.__included_in_dataset_layout = QVBoxLayout()
        
        self.category_number = "8"
        self.training_count_number = "2000"
        self.test_image_count_number= "2800"
        self.total_image_count_number= "5600"
        
        self.__categorie_text = 'Category count: '
        self.__training_text = 'Training image count: '
        self.__test_image_text = 'Test image count: '
        self.__totale_image_text = 'Total image count: '

        self.__categorie_info = QLabel(self.category_number)
        self.__training_info = QLabel(self.training_count_number)
        self.__test_image_info = QLabel(self.test_image_count_number)
        self.__totale_image_info = QLabel(self.total_image_count_number)

        self.cat_count = self.__text_tgt(self.__categorie_text, self.__categorie_info)
        self.train_count = self.__text_tgt(self.__training_text, self.__training_info)
        self.test_count = self.__text_tgt(self.__test_image_text, self.__test_image_info)
        self.totale_count = self.__text_tgt(self.__totale_image_text, self.__totale_image_info)

        
        self.__included_in_dataset_layout.addLayout(self.cat_count)
        self.__included_in_dataset_layout.addLayout(self.train_count)
        self.__included_in_dataset_layout.addLayout(self.test_count)
        self.__included_in_dataset_layout.addLayout(self.totale_count)
        
        self.__included_in_dataset_box.setLayout(self.__included_in_dataset_layout)
       
        ########### Dataset - transformation ################
        self.__transformation_box = QtWidgets.QGroupBox('Transformation')
        self.__transformation_layout = QVBoxLayout()

        # Texte dans Label
        self.__translated_text = 'Translated: '
        self.__rotated_text = 'Rotated: '
        self.__scaled_text = 'Scaled: '
        
        # Texte dans les inputs du label
        self.translate = "True"
        self.rotate = "True"
        self.scale = "True"
        
        # init de label
        self.__translated_info = QLabel(self.translate)
        self.__rotated_info = QLabel(self.rotate)
        self.__scaled_info = QLabel(self.scale)

        # Rassemble les Label et les inputs
        self.translated = self.__text_tgt(self.__translated_text, self.__translated_info)
        self.rotated = self.__text_tgt(self.__rotated_text, self.__rotated_info)
        self.scaled = self.__text_tgt(self.__scaled_text, self.__scaled_info)
        
        self.__transformation_layout.addLayout(self.translated)
        self.__transformation_layout.addLayout(self.rotated)
        self.__transformation_layout.addLayout(self.scaled)
         
        self.__transformation_box.setLayout(self.__transformation_layout)
        
        self.__central_layout_data = QVBoxLayout()
        self.__central_layout_data.addLayout(self.__menu_list_data_layout)
        self.__central_layout_data.addWidget(self.__included_in_dataset_box)
        self.__central_layout_data.addWidget(self.__transformation_box)
        self.__group_data_set.setLayout(self.__central_layout_data)
 

        # ---------------------------- (single test) - Global menu --------------------------------#    
        
        self.__group_single_test = QtWidgets.QGroupBox('Single test')
           
        # single test - list deroulante
        self.__menu_list_single_layout = QVBoxLayout()
        self.__menu_single_list = QtWidgets.QComboBox()
        self.__menu_list_single_layout.addWidget(self.__menu_single_list)

        # single test - image
        self.__image_single_layout = QVBoxLayout()
        self.__single_background_color = QLabel()
        self.__single_background_color.alignment = Qt.AlignCenter
        self.__single_background_color.setFixedHeight(90)        

        pixmap = QtGui.QPixmap(self.__single_background_color.size())
        pixmap.fill(QtGui.QColor(56, 68, 110))
    
        self.__single_background_color.setPixmap(pixmap)

        self.__image_single_layout.addWidget(self.__single_background_color)

        # single test - Classify button
        self.__classify_button_layout = QVBoxLayout()
        self.__classify_button = QtWidgets.QPushButton('Classify')
        self.__classify_button_layout.addWidget(self.__classify_button)
        self.__classify_button.clicked.connect(self.classifyClicked)

        # champ text
        self.__classify_info_layout = QVBoxLayout()
        self.classify = "not classified"
        self.__classify_info = QLabel(self.classify)
        self.__classify_info.alignment = Qt.AlignCenter 
        self.__classify_info_layout.addWidget(self.__classify_info)


        central_layout_single = QVBoxLayout()
        central_layout_single.addLayout(self.__menu_list_single_layout)
        central_layout_single.addLayout(self.__image_single_layout)
        central_layout_single.addLayout(self.__classify_button_layout)
        central_layout_single.addLayout(self.__classify_info_layout)
        self.__group_single_test.setLayout(central_layout_single)
    
        
        # ---------------------------- (KNN parametre) - Global menu --------------------------------#    

        self.__group_knn_parameters = QtWidgets.QGroupBox('KNN parameters')
        self.__knn_scrollbar = QtWidgets.QScrollBar()
        self.__max_scrollbar = QtWidgets.QScrollBar() 
        self.__parametre_info_layout = QVBoxLayout()
    
        scroll_1_layout = self.__create_channel('K =', self.__knn_scrollbar, 125, 3)
        scroll_2_layout = self.__create_channel('Max dist =', self.__max_scrollbar, 125, 100)

        self.__parametre_info_layout.addLayout(scroll_1_layout)
        self.__parametre_info_layout.addLayout(scroll_2_layout)


        central_layout_parametres = QVBoxLayout()
        central_layout_parametres.addLayout(self.__parametre_info_layout)
        self.__group_knn_parameters.setLayout(central_layout_parametres)
     
    
        # ------------------------------------------ About ---------------------------------------#    
        self.__about_button_layout = QVBoxLayout()
        self.__about_button = QtWidgets.QPushButton('About')
        self.__about_button.clicked.connect(self.popup_about)
        
        # ------------------------------------------ GAME KNN  ---------------------------------------#    
        self.__data1 = MyData(100)
        self.__data2 = MyData(100)
        self.__data1.randomize_normal(-2.5, 1.5)
        self.__data2.randomize_normal(2.5, 3.5)
        
        self.__scatter = ScatterDiagram(self.__data1, self.__data2)
        
        self.__action = QtWidgets.QPushButton('Randomize')
        
        Knn_widget = QtWidgets.QWidget()
        central_Knn_layout = QtWidgets.QVBoxLayout(Knn_widget)
        
        central_Knn_layout.addWidget(self.__scatter.widget)
        central_Knn_layout.addWidget(self.__action)

        self.__knn_view = QLabel("KNN")
        self.__knn_view.setFixedWidth(600)
        self.__knn_view.setFixedHeight(600)
        self.__knn_view.alignment = Qt.AlignCenter
        

        # ------------------------------------------ GLOBAL ---------------------------------------#    
        self.setWindowTitle('KNN Image Classifaction')
        
        self.__setting_box = QVBoxLayout()
        self.__setting_box.addWidget(self.__group_data_set)
        self.__setting_box.addWidget(self.__group_single_test)
        self.__setting_box.addWidget(self.__group_knn_parameters)
        self.__setting_box.addWidget(self.__about_button)
  
        self.__Knn_box = QVBoxLayout()
        self.__Knn_box.addWidget(Knn_widget)
        
        self.__principal_box = QHBoxLayout()
        self.__principal_box.addLayout(self.__setting_box)
        self.__principal_box.addLayout(self.__Knn_box)
        

        centrale_widget = QWidget()
        centrale_widget.setLayout(self.__principal_box)
        self.getconnection()
        self.setCentralWidget(centrale_widget)
      
    def __create_channel(self, text, scroll, width, range):
        title = QLabel(text)
        value = QLabel('0')
        
        title.setFixedWidth(60)
        scroll.setMinimumWidth(2 * width)
        scroll.setOrientation(Qt.Horizontal)
        scroll.setRange(0,range)
        scroll.setValue(0)
        value.setFixedWidth(20)
        
        scroll.valueChanged.connect(value.setNum)
        
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(value)
        layout.addWidget(scroll)
       
        return layout

    # prend le label et la valeur et l'affiche ensemble
    def __text_tgt(self, text, ok):
        title = QLabel(text)
        value = ok
       
        
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(value)

        return layout     
    
       
    
    def getconnection(self):
        try:
            #AAAaaa123
            connection = psycopg2.connect("dbname=postgres user=postgres port=5432 password=admin")
        except psycopg2.Error as e:
            print("Unable to connect!", e.pgerror, e.diag.message_detail)
                
        else:
            print("Connected!!!")
            self.update(connection)
            
            #connection.close()
            return connection
        pass
        
    def update(self,connection):
        self.cur = connection.cursor()
        self.cur.execute("SELECT name FROM klustr.data_set_info;")
        
        for i, emp in enumerate(self.cur):
            self.__menu_data_list.addItem(emp[0])
           
        
        self.__menu_data_list.currentIndexChanged.connect(self.selectedDataset)
        self.__menu_data_list.currentIndexChanged.connect(self.single_test_dataset)
        self.__menu_single_list.currentIndexChanged.connect(self.change_tumbnail)
    
    # on affiche le tous les image lier au dataset dans le menu single list
    @Slot()
    def single_test_dataset(self):
        self.__menu_single_list.clear()
        currentSelectedItem = self.__menu_data_list.currentText()

        
        self.cur.execute("SELECT id from klustr.data_set WHERE NAME = %s",(currentSelectedItem,))
        id = self.cur.fetchone()
        
        self.cur.execute("SELECT name from klustr.image where ID IN (select image from klustr.data_set_training where data_set = %s)",(id[0],))
        list = self.cur.fetchall()
        
        for i,item in enumerate(list):
            self.__menu_single_list.addItem(item[0])
        

    @Slot()
    def classifyClicked(self):
        liste_metrique_test = np.empty((0,3), dtype=np.float64)
        liste_metrique_training = np.empty((0, 4), dtype=np.float64)
        data_set_name = self.__menu_data_list.currentText()
        current_selected_image = self.__menu_single_list.currentText()
        
        # pour recevoir tous les images d'un dataset
        self.cur.execute("SELECT id FROM klustr.data_set WHERE NAME = %s",(data_set_name,))
        id = self.cur.fetchone()
        self.cur.execute("SELECT img_data,name FROM klustr.image WHERE ID IN (SELECT image FROM klustr.data_set_test WHERE data_set = %s)",(id[0],))
        listImages = self.cur.fetchall()

        # on recupère l'image qu'on veut tester
        self.cur.execute("SELECT img_data FROM klustr.image WHERE NAME = %s",(current_selected_image,))
        imageData = self.cur.fetchone()
        knn = KNN(3,imageData[0])
        
        for image in listImages:
            imageBinary = knn.conversion_png_ndarray(image[0])
            complexite = knn.calcul_complexite(imageBinary)
            ratio_circularite = knn.calcul_ratio_circularite(imageBinary)
            ratio_distance_image = knn.calcul_ratio_distance_image(imageBinary)
            liste_metrique_training = np.append(liste_metrique_training,complexite)
            liste_metrique_training = np.append(liste_metrique_training,ratio_circularite)
            liste_metrique_training = np.append(liste_metrique_training,ratio_distance_image)
            
        knn.set_liste_metriques_dataset(liste_metrique_training.reshape(-1,3))
        
        imageBinary = knn.conversion_png_ndarray(knn.image_test)
        complexite = knn.calcul_complexite(imageBinary)
        ratio_circularite = knn.calcul_ratio_circularite(imageBinary)
        ratio_distance_image = knn.calcul_ratio_distance_image(imageBinary)
        liste_metrique_test = np.append(liste_metrique_test,complexite)
        liste_metrique_test = np.append(liste_metrique_test,ratio_circularite)
        liste_metrique_test = np.append(liste_metrique_test,ratio_distance_image)
    
        knn.set_metrique_image_test(liste_metrique_test.reshape(-1,3))
    
        knn.set_nb_voisins(self.__knn_scrollbar.value)
    
        knn.set_distance(knn.calculer_distance_image_test_dataset(
            knn.liste_metriques_dataset,knn.metrique_image_test,knn.nb_voisins))
    
        print(f"la/les distances les plus proche sont {knn.distance} soit les {knn.nb_voisins} voisins les plus proches")
        
        # on arrive à calculer les voisins les plus proches avec les distances
        # le problème est de savoir qu'elle est le nom de ou les images correspondants à ces voisins
        # aussi le graphique ne se met pas à jour

    # changer le tumbnail du text
    @Slot()
    def change_tumbnail(self):
        value = self.__menu_single_list.currentText()
        
        if value != "":
            self.cur.execute("SELECT img_thumbnail FROM klustr.image WHERE NAME = %s",(value,))
            data = self.cur.fetchone()
            qimage = QtGui.QImage.fromData(bytearray(data[0]))
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.__single_background_color.setPixmap(pixmap)

    # afficher les donnes relative au data_set selectionner
    @Slot()
    def selectedDataset(self):
        currentSelectedItem = self.__menu_data_list.currentText()

        self.cur.execute("SELECT * FROM klustr.data_set_info WHERE NAME = %s", (currentSelectedItem,))
        value = self.cur.fetchone() 
        self.translate = str(value[2])
        self.rotate = str(value[3])
        self.scale = str(value[4])
        self.category = str(value[5])
        self.training_count = str(value[6])
        self.test_image_count = str(value[7])
        self.total_image_count = str(value[8])
        
        
        self.__translated_info.setText(self.translate) # translated
        self.__rotated_info.setText(self.rotate)
        self.__scaled_info.setText(self.scale)
        self.__categorie_info.setText(self.category)
        self.__training_info.setText(self.training_count)
        self.__test_image_info.setText(self.test_image_count)
        self.__totale_image_info.setText(self.total_image_count)     
    

    # execute commande SQL pour afficher les infos spécifique 
   
    def popup_about(self):
        about_text = """Ce logiciel est le premier projet du cours C52
        
        Il a été réalisé par :
          - Kevin Gbeti
          - Lemar Andar
          - Elyas Kaouah
          - Rayane Rachid Kennaf
          
        Il consiste à executer l'algorithme KNN avec les concepts suivants:
          - Le calcul de distance entre un point et ses voisins.
          - Prendre le nombre k de voisins, en fait la moyenne et détermine la classe d'image à laquelle l'image test appartient. 
          
        Nos 3 descripteurs de forme sont :
          - Complexite
             - correspondant au ratio entre l'aire de la forme / permiètre au carre de la forme
          - Ratio de Circularite
             - correspondant au ratio entre le cercle inscrit et le cercle circonscrit
          - Ratio de Distance
             - correspondant au ratio entre la distance minimum du centroide à la distance la plus courte
             - divise par la distance maximum du centroide à la distance la plus longue
             
        Plus précisément, ce laboratoire permet de mettre en pratique les notions de :
          - Matplotlib
          - Numpy
          - DataBase(pgAdmin - posgresql)
          - PyQt_Pyside6 
          
        Un effort d'abstraction a été fait pour ces points:
          - Trouver le second descripteur de forme 
          - Trouver un moyen d'optimiser le KNN sans aucune utilisation de for loop (python)
          """
        QtWidgets.QMessageBox.about(self,"KlustR KNN Classifier", about_text)
            
def main():
    app = QtWidgets.QApplication(sys.argv)

    w = myApp()
    w.show()
    
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()