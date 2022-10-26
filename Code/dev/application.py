import sys
from tkinter import CENTER, HORIZONTAL
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QScrollBar, QVBoxLayout, QHBoxLayout
import random

from __feature__ import snake_case, true_property


class myApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
         
        # ---------------------------- (Dataset) - Global menu--------------------------------#
        self.__group_data_set = QtWidgets.QGroupBox('Dataset')
        
        
        # Dataset - list deroulante
        self.__menu_list_data_layout = QVBoxLayout()
        self.__menu_data_list = QtWidgets.QComboBox()
        self.__menu_list_data_layout.add_widget(self.__menu_data_list)
        
        
        # Dataset - included in dataset
        self.__included_in_dataset_box = QtWidgets.QGroupBox('Included in dataset')
        self.__included_in_dataset_layout = QVBoxLayout()
        
        
        self.__categorie_info = QLabel('Category count:      9')
        self.__trainning_info = QLabel('Training image count:     126')
        self.__test_image_info = QLabel('Test image count:     189')
        self.__totale_image_info = QLabel('Total image count:     315')
        
        self.__included_in_dataset_layout.add_widget(self.__categorie_info)
        self.__included_in_dataset_layout.add_widget(self.__trainning_info)
        self.__included_in_dataset_layout.add_widget(self.__test_image_info)
        self.__included_in_dataset_layout.add_widget(self.__totale_image_info)
        
        self.__included_in_dataset_box.set_layout(self.__included_in_dataset_layout)
       
        
        # Dataset - transformation
        self.__transformation_box = QtWidgets.QGroupBox('Transformation')
        self.__transformation_layout = QVBoxLayout()

        self.__translated_info = QLabel('Translated:    true')
        self.__rotaded_info = QLabel('Rotated:     true')
        self.__scladed_info = QLabel('Scaled:      true')
        
        self.__transformation_layout.add_widget(self.__translated_info)
        self.__transformation_layout.add_widget(self.__rotaded_info)
        self.__transformation_layout.add_widget(self.__scladed_info)
         
        
        self.__transformation_box.set_layout(self.__transformation_layout)
        
        
        
        central_layout_data = QVBoxLayout()
        central_layout_data.add_layout(self.__menu_list_data_layout)
        central_layout_data.add_widget(self.__included_in_dataset_box)
        central_layout_data.add_widget(self.__transformation_box)
        self.__group_data_set.set_layout(central_layout_data)
 

        # ---------------------------- (single test) - Global menu --------------------------------#    
        
        self.__group_single_test = QtWidgets.QGroupBox('Single test')
           
        # single test - list deroulante
        self.__menu_list_single_layout = QVBoxLayout()
        self.__menu_single_list = QtWidgets.QComboBox()
        self.__menu_list_single_layout.add_widget(self.__menu_single_list)

        # single test - image
        self.__image_single_layout = QVBoxLayout()
        self.__single_background_color = QLabel()
        self.__single_background_color.alignment = Qt.AlignCenter
        self.__single_background_color.set_fixed_height(90)
        

        pixmap = QtGui.QPixmap(self.__single_background_color.size)
        pixmap.fill(QtGui.QColor(56, 68, 110))
    
        self.__single_background_color.set_pixmap(pixmap)

        self.__image_single_layout.add_widget(self.__single_background_color)

        # single test - Classify button
        self.__classify_button_layout = QVBoxLayout()
        self.__classify_button = QtWidgets.QPushButton('Classify')
        self.__classify_button_layout.add_widget(self.__classify_button)

        # champ text
        self.__classify_info_layout = QVBoxLayout()

        self.__classify_info = QLabel('star_5_050')
        self.__classify_info.alignment = Qt.AlignCenter 
        self.__classify_info_layout.add_widget(self.__classify_info)


        central_layout_single = QVBoxLayout()
        central_layout_single.add_layout(self.__menu_list_single_layout)
        central_layout_single.add_layout(self.__image_single_layout)
        central_layout_single.add_layout(self.__classify_button_layout)
        central_layout_single.add_layout(self.__classify_info_layout)
        self.__group_single_test.set_layout(central_layout_single)
        
        
    
        
        # ---------------------------- (KNN parametre) - Global menu --------------------------------#    

        self.__group_knn_parameters = QtWidgets.QGroupBox('KNN parameters')
        self.__knn_scrollbar = QtWidgets.QScrollBar()
        self.__max_scrollbar = QtWidgets.QScrollBar() 
        self.__parametre_info_layout = QVBoxLayout()

    
        scroll_1_layout = self.__create_channel('k =', self.__knn_scrollbar,75)
        scroll_2_layout = self.__create_channel('kd =', self.__max_scrollbar,75)

        self.__parametre_info_layout.add_layout(scroll_1_layout)
        self.__parametre_info_layout.add_layout(scroll_2_layout)


        central_layout_parametres = QVBoxLayout()
        central_layout_parametres.add_layout(self.__parametre_info_layout)
        self.__group_knn_parameters.set_layout(central_layout_parametres)
     
    
        # ------------------------------------------ About ---------------------------------------#    
        self.__about_button_layout = QVBoxLayout()
        self.__about_button = QtWidgets.QPushButton('About')
        

        # ------------------------------------------ GAME ---------------------------------------#    

        self.__knn_view = QLabel("KNN")
        self.__knn_view.set_fixed_width(600)
        self.__knn_view.set_fixed_height(600)
        self.__knn_view.alignment = Qt.AlignCenter
        

        # ------------------------------------------ GLOBAL ---------------------------------------#    

        self.__setting_box = QVBoxLayout()
        self.__setting_box.add_widget(self.__group_data_set)
        self.__setting_box.add_widget(self.__group_single_test)
        self.__setting_box.add_widget(self.__group_knn_parameters)
        self.__setting_box.add_widget(self.__about_button)
  
        self.__Knn_box = QVBoxLayout()
        self.__Knn_box.add_widget(self.__knn_view)
        
        self.__principal_box = QHBoxLayout()
        self.__principal_box.add_layout(self.__setting_box)
        self.__principal_box.add_layout(self.__Knn_box)

        self.set_window_title('KNN Image Classification')

        centrale_widget = QWidget()
        centrale_widget.set_layout(self.__principal_box)
        self.set_central_widget(centrale_widget)
      
    def __create_channel(self, text, scroll, width):
        title = QLabel(text)
        value = QLabel('0')
        
        title.set_fixed_width(22)
        scroll.minimum_width = 2 * width
        scroll.orientation = Qt.Horizontal
        scroll.set_range(0, 255)
        scroll.value = 0
        value.alignment = Qt.AlignCenter
        value.set_fixed_width(22)
           
        layout = QHBoxLayout()
        layout.add_widget(title)
        layout.add_widget(value)
        layout.add_widget(scroll)
       
        return layout
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)

    w = myApp()
    w.show()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()