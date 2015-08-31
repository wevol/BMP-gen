# -*- coding:utf-8 -*-
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from bmp_gen_gui import  UiBitmapGenerator
from bmp_gen_exec import Pictures


class BitmapGen(QtWidgets.QDialog):
    """GUI tool to build BMP picture by repeating small pattern.

    Attributes:
        border : A dictionary stores integer resolutions of BMP picture
	    and pattern.
        pattern : A less or equal 4 x 4 x 3 array of Pattern data values.
            Data values are integer between 0 and 255.
    """
    def __init__(self, parent=None):
        """Inits GUI windows"""
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = UiBitmapGenerator()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.store_input)

    def store_input(self):
        """Store data values from GUI."""
        try:
            self.border = {
                       "horizontal":int(self.ui.lineEdit_horizontal.text()),
                       "vertical":int(self.ui.lineEdit_vertical.text()),
                       "pattern_x":int(self.ui.lineEdit_x.text()),
                       "pattern_y":int(self.ui.lineEdit_y.text())
                        }
        except ValueError:
            QtWidgets.QMessageBox.information(
	        self, "Error", "Resolution or Pattern is not Integer")
        else:
            pattern = np.uint8(np.linspace(
	        0, 0,
                self.border["pattern_x"] * 3 * self.border["pattern_y"] ))
            pattern.shape = (self.border["pattern_y"], 
	                    self.border["pattern_x"] * 3)
        try:
            for x in range(self.border["pattern_x"] *3):
                for y in range(self.border["pattern_y"]):
                    pattern[y,x] = int(self.ui.tableWidget.item(y,x).text())
        except ValueError:
            QtWidgets.QMessageBox.information(self,"Error",
	                                      "RGB is not a Integer")
        except AttributeError:
            QtWidgets.QMessageBox.information(
	        self,"Error", "Pattern has to be less or equal to 4x4")
        else:
            pattern.shape = (self.border["pattern_y"], 
	                    self.border["pattern_x"], 3)
        filename = self.ui.lineEdit_Filename.text()
        self.check_input(pattern, filename)

    def check_input(self, pattern, filename):
        """Check input values are reasonable or not.
	    
	Check the dimention of Pattern array is less than the one of 
	BMP picture.
        Check filename is not empty.
        """ 
        if (self.border["horizontal"] < self.border["pattern_x"] or
	    self.border["vertical"] < self.border["pattern_x"]):
            QtWidgets.QMessageBox.information(
	        self, "Error", "Resolution has to be larger than Pattern")
        elif not filename:
            QtWidgets.QMessageBox.information(
                self,"Error", "Please input File Name")
        else:
            self.gen(pattern, filename)

    def gen(self, pattern, filename):
        """Generate BMP picture.
	    
        Expand basic Pattern array to a .bmp file.
        Build array of BMP picture by repeat Pattern Array.

        Args:
            border : A dictionary stores integer resolutions of BMP
		    picture and pattern.
            pattern : A less or equal 4 x 4 x 3 array of Pattern data
		    values. Data values are integer between 0 and 255.
        """
        image = Pictures(
        self.border["horizontal"],
        self.border["vertical"],
        self.border["pattern_x"],
        self.border["pattern_y"],
        pattern)
        image.picture_create(filename + ".bmp")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = BitmapGen()
    myapp.show()
    sys.exit(app.exec_())
