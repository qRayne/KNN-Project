from cgitb import text
from email.mime import image
import sys
from tkinter import CENTER, HORIZONTAL
from turtle import right, st
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QScrollBar, QVBoxLayout, QHBoxLayout
import random

from __feature__ import snake_case, true_property


class myApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
         
        # Dataset
        self.__group_data_set = QtWidgets.QGroupBox('Dataset')
        
        
        # Dataset - list deroulante
        self.__menu_list_layout = QVBoxLayout()
        self.__menu_list = QtWidgets.QComboBox()
        self.__menu_list_layout.add_widget(self.__menu_list)
        
        
        # Dataset - included in dataset
        self.__included_in_dataset_box = QtWidgets.QGroupBox('included in dataset')
        self.__included_in_dataset_layout = QVBoxLayout()
        
        
        self.__categorie_info = QLabel('Category count:      9')
        self.__trainning_info = QLabel('Trainning image count:     126')
        self.__test_image_info = QLabel('Test images count:     189')
        self.__totale_image_info = QLabel('Total images count:     315')
        
        self.__included_in_dataset_layout.add_widget(self.__categorie_info)
        self.__included_in_dataset_layout.add_widget(self.__trainning_info)
        self.__included_in_dataset_layout.add_widget(self.__test_image_info)
        self.__included_in_dataset_layout.add_widget(self.__totale_image_info)
        
        self.__included_in_dataset_box.set_layout(self.__included_in_dataset_layout)
       
        
        # Dataset - transformation
        self.__transformation_box = QtWidgets.QGroupBox('Transformation')
        self.__transformation_layout = QVBoxLayout()

        self.__translated_info = QLabel('Translated:    true')
        self.__rotaded_info = QLabel('rotaded:     true')
        self.__scladed_info = QLabel('scladed:      true')
        
        self.__transformation_layout.add_widget(self.__translated_info)
        self.__transformation_layout.add_widget(self.__rotaded_info)
        self.__transformation_layout.add_widget(self.__scladed_info)
         
        
        self.__transformation_box.set_layout(self.__transformation_layout)
        
        
        
        # --------
        central_layout = QVBoxLayout()
        central_layout.add_layout(self.__menu_list_layout)
        central_layout.add_widget(self.__included_in_dataset_box)
        central_layout.add_widget(self.__transformation_box)
        self.__group_data_set.set_layout(central_layout)
      
      
      
    
        # single test 
        self.__group_single_test = QtWidgets.QGroupBox('single test')
        
        
        
        
        
        
        
        self.__group_knn_parameters = QtWidgets.QGroupBox('knn parameters')
        
        self.__principal_box = QVBoxLayout()
        self.__principal_box.add_widget(self.__group_data_set)
        self.__principal_box.add_widget(self.__group_single_test)
        self.__principal_box.add_widget(self.__group_knn_parameters)
        self.__principal_box.add_stretch()
        
        centrale_widget = QWidget()
        centrale_widget.set_layout(self.__principal_box)
        self.set_central_widget(centrale_widget)
      
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)

    w = myApp()
    w.show()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()