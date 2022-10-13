from os import wait
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image, ImageOps
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPainter, QBrush, QPen
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from os.path import isfile, join, basename


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, radius, output_dir, parent=None):
        super().__init__(parent)
        
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        self.r = radius
        self.output_dir = output_dir

        self.x_list = []
        self.y_list = []

        self.path_list = QFileDialog.getOpenFileNames(self)[0]

        first_image = self.path_list[0]
        self.setPixmap(QtGui.QPixmap(first_image))
        

    @property
    def pixmap_item(self):
        return self._pixmap_item

    def setPixmap(self, pixmap):
        self.pixmap_item.setPixmap(pixmap)

    def resizeEvent(self, event):
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if self.pixmap_item is self.itemAt(event.pos()):
            sp = self.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp).toPoint()
            print(lp)
            pen = QPen(Qt.red, 5, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
            self.scene.addEllipse(lp.x()-self.r, lp.y()-self.r, self.r*2, self.r*2, pen = pen)
            self.x_list.append(lp.x())
            self.y_list.append(lp.y())
    
    def get_xy(self):
        return self.x_list, self.y_list
    
    def keyPressEvent(self, qKeyEvent):
        #print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.find_ice_temp(self.path_list)
            self.close()
        else:
            super().keyPressEvent(qKeyEvent)

    def find_ice_temp(self, path_list):
        
        file_name_list = []
        date_time_list = []
        gss_table = []

        print(len(path_list))

        for i in np.arange(len(path_list)):
            
            image = Image.open(path_list[i])
            red, green, blue = image.split()
            image_exif = image.getexif()
            image_datetime = image_exif[306]
            image_gs = ImageOps.grayscale(red)
            image_gs_array = np.array(image_gs)

            print(image_datetime)
            
            gss_list = []
            for j in np.arange(len(self.x_list)):
                x = self.x_list[j]
                y = self.y_list[j]
                a_mask = GraphicsView.create_circular_mask(np.shape(image_gs_array)[0], np.shape(image_gs_array)[1], center = [x, y], radius=self.r)
                gray_scale_sum = np.sum(a_mask * image_gs_array)
                gss_list.append(gray_scale_sum)
            
            file_name_list.append(basename(path_list[i]))
            date_time_list.append(image_datetime)
            gss_table.append(gss_list)
        
        self.plot_a_droplet(gss_table, date_time_list)

        #np.savetxt(join(self.output_dir, "gss_table.csv"), gss_table, delimiter=',')

        
        with open(join(self.output_dir, "gss_table.csv"), 'w') as the_file:
            for i in np.arange(len(date_time_list)):
                the_file.write(file_name_list[i])
                the_file.write(", ")
                the_file.write(date_time_list[i])
                for j in np.arange(len(gss_table[i])):
                    the_file.write(", ")
                    the_file.write(str(gss_table[i][j]))
                the_file.write("\n")

    
    def plot_a_droplet(self, gss_table, date_time_list, n = 0):
        #print(len(date_time_list))
        plt.plot(np.arange(len(date_time_list)), gss_table[:])
        plt.show()

    def create_circular_mask(h, w, center=None, radius=None):
        if center is None: # use the middle of the image
            center = (int(w/2), int(h/2))
        if radius is None: # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w-center[0], h-center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
        mask = dist_from_center <= radius
        return mask

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    output_dir = "/Users/bochen/TAMU/Ice nucleation detection/fucoxanthin 5mgml/output_brightness"
    circle_size = 22

    w = GraphicsView(circle_size, output_dir)
    w.show()

    sys.exit(app.exec())
    


