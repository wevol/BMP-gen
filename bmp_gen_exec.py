# -*- coding:utf-8 -*-
import sys
import numpy as np
from PIL import Image


class Pictures(object):
    """ Expand basic Pattern to a .bmp file

    Re-produce less than 4x4 pixels data to a whole new BMP file.

    Attributes:
      horizontal : BMP file horizotnal pixel resolution. Intger value.
      vertical : BMP file vertical pixel resolution. Integer value.
      pattern_x : basic pattern horizontal pixel resolution. 
          Integer value between 1 and 4
      pattern_y : basic pattern vertical pixel resolution.
          Integer value between 1 and 4
      pattern_in : 3 dimentional Array data , maximum 4 x 4 x 3
          with integer value between 0 and 255
    """
    def __init__(self, horizontal, vertical, pattern_x, pattern_y,
                 pattern_in, parent=None):
        """Inits resolution values and create Pattern."""
        self.horizontal = int(horizontal)
        self.vertical = int(vertical)
        self.pattern_x = int(pattern_x)
        self.pattern_y = int(pattern_y)
        self.pattern_layout()
        self.pattern_create(pattern_in)
        self.picture_layout()
	
    def pattern_layout(self):
        """Build array of Pattern"""
        self.pattern = np.uint8(np.linspace(0,0,
                                self.pattern_x * self.pattern_y *3))
        self.pattern.shape = self.pattern_y, self.pattern_x, 3
	
    def pattern_create(self, pattern_in):
        """Store values into Pattern array"""
        self.pattern = pattern_in	
	
    def picture_layout(self):
        """Build array of BMP picture by repeat Pattern array"""
        self.picture = np.tile(self.pattern,
                              (int(self.vertical/self.pattern_y),
                               int(self.horizontal/self.pattern_x),1))
	
    def picture_create(self, filename):
        """Save BMP picture array to file"""
        img = Image.fromarray(self.picture, "RGB")
        img.save(filename)

if __name__ == "__main__":
    image = Pictures(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    image.picture_create(sys.argv[1] + ".bmp")
