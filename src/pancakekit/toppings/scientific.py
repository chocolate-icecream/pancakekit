import numpy as np
from PIL import PILImage
from ..pancakekit import ImageBox
from ..utils import *
from matplotlib import cm


class ArrayToImageBox(ImageBox):
    def prepare(self, array=None, range_min=None, range_max=None, colormap="nipy_spectral"):
        super().prepare(max_length=None)
        self.range_min = range_min
        self.range_max = range_max
        self.array = None
        self._roi = None
        
        if "greyscale" in self.arguments or "grayscale" in self.arguments:
            colormap = "gray"
            
        self.colormap = getattr(cm, colormap)
        self.set(array)
    
    def set_colormap(self, colormap="nipy_spectral"):
        self.colormap = getattr(cm, colormap)
    
    def set(self, array=None, range_min=None, range_max=None):
        if isinstance(array, str):
            file_name = array
            image = PILImage.open(file_name)
            if image.mode not in ["L", "I", "F", "I;16", "I;16L", "I;16B", "I;16N"]:
                image = image.convert("L")
            array = np.array(image)
                
                
        if array is None and self.array is None:
            array = np.array([[0, 0],[0, 0]])
        if array is None:
            array = self.array
        else:
            self.array = array.copy()
        
        self.range_min = range_min if range_min is not None else self.range_min
        self.range_max = range_max if range_max is not None else self.range_max
            
        range_max = np.nanmax(array) if self.range_max is None else self.range_max
        range_min = np.nanmin(array) if self.range_min is None else self.range_min
        if range_max == range_min:
            range_max += 0.0
            range_min -= 1
        
        if self._roi is not None:
            array = array[self._roi[0]:self._roi[2],self._roi[1]:self._roi[3]]
        
        array = (255*self.colormap((array-range_min)/(range_max - range_min))).astype(np.uint8)
        image = PILImage.fromarray(array)
        super().set(image)
    
    def set_range(self, range_min=None, range_max=None):
        self.range_min = range_min
        self.range_max = range_max
        self.set()
        
    @property
    def roi(self): #
        return self._roi
    @roi.setter
    def roi(self, value):
        self._roi = value
        self.set()