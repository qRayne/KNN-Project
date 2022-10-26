import sys
from tkinter import HORIZONTAL

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


from cgitb import text
from email.mime import image
from turtle import right, st
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout


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
        axes.set_xlabel('X-axis', fontweight='bold')
        axes.set_ylabel('Y-axis', fontweight='bold')
        axes.set_zlabel('Z-axis', fontweight='bold')
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
    
    
class myApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
         
        # ---------------------------- (Dataset) - Global menu--------------------------------#
        self.__group_data_set = QtWidgets.QGroupBox('Dataset')
        
        
        # Dataset - list deroulante
        self.__menu_list_data_layout = QVBoxLayout()
        self.__menu_data_list = QtWidgets.QComboBox()
        self.__menu_list_data_layout.addWidget(self.__menu_data_list)
        
        
        # Dataset - included in dataset
        self.__included_in_dataset_box = QtWidgets.QGroupBox('Included in dataset')
        self.__included_in_dataset_layout = QVBoxLayout()
        
        
        self.__categorie_info = QLabel('Category count:      9')
        self.__trainning_info = QLabel('Training image count:     126')
        self.__test_image_info = QLabel('Test image count:     189')
        self.__totale_image_info = QLabel('Total image count:     315')
        
        self.__included_in_dataset_layout.addWidget(self.__categorie_info)
        self.__included_in_dataset_layout.addWidget(self.__trainning_info)
        self.__included_in_dataset_layout.addWidget(self.__test_image_info)
        self.__included_in_dataset_layout.addWidget(self.__totale_image_info)
        
        self.__included_in_dataset_box.setLayout(self.__included_in_dataset_layout)
       
        
        # Dataset - transformation
        self.__transformation_box = QtWidgets.QGroupBox('Transformation')
        self.__transformation_layout = QVBoxLayout()

        self.__translated_info = QLabel('Translated:    true')
        self.__rotaded_info = QLabel('Rotated:     true')
        self.__scladed_info = QLabel('Scaled:      true')
        
        self.__transformation_layout.addWidget(self.__translated_info)
        self.__transformation_layout.addWidget(self.__rotaded_info)
        self.__transformation_layout.addWidget(self.__scladed_info)
         
        
        self.__transformation_box.setLayout(self.__transformation_layout)
        
        
        
        central_layout_data = QVBoxLayout()
        central_layout_data.addLayout(self.__menu_list_data_layout)
        central_layout_data.addWidget(self.__included_in_dataset_box)
        central_layout_data.addWidget(self.__transformation_box)
        self.__group_data_set.setLayout(central_layout_data)
 

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

        # champ text
        self.__classify_info_layout = QVBoxLayout()

        self.__classify_info = QLabel('star_5_050')
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

    
        scroll_1_layout = self.__create_channel('K =', self.__knn_scrollbar,125, 3)
        scroll_2_layout = self.__create_channel('Max dist =', self.__max_scrollbar,125,100)

        self.__parametre_info_layout.addLayout(scroll_1_layout)
        self.__parametre_info_layout.addLayout(scroll_2_layout)


        central_layout_parametres = QVBoxLayout()
        central_layout_parametres.addLayout(self.__parametre_info_layout)
        self.__group_knn_parameters.setLayout(central_layout_parametres)
     
    
        # ------------------------------------------ About ---------------------------------------#    
        self.__about_button_layout = QVBoxLayout()
        self.__about_button = QtWidgets.QPushButton('About')
        

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

        self.setWindowTitle('Knn Image Classifaction')
        
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
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)

    w = myApp()
    w.show()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()