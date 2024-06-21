from PIL import  ImageOps, ImageFilter, ImageChops
"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

def binarizar(img):
    return img.convert('L')

def erosion(img):
    binarizada = binarizar(img)
    return binarizada.filter(ImageFilter.MinFilter(3))

def dilatacion(img):
    binarizada = binarizar(img)
    return binarizada.filter(ImageFilter.MaxFilter(3))

def apertura(img):
    binarizada = binarizar(img)
    return binarizada.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))

def clausura(img):
    binarizada = binarizar(img)
    return binarizada.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))

def polarizar(img):
    binarizada = binarizar(img)
    return ImageOps.invert(binarizada)
    
def eliminarRuido(img):
    binarizada = binarizar(img)
    #Clausura
    binarizada = binarizada.filter(ImageFilter.MaxFilter(3))
    binarizada = binarizada.filter(ImageFilter.MinFilter(3))
        
    #Apertura
    binarizada = binarizada.filter(ImageFilter.MinFilter(3))
    binarizada = binarizada.filter(ImageFilter.MaxFilter(3))
        
    return binarizada

def resaltarBordes(img):
    binarizada = binarizar(img)
    dilatacion = binarizada.filter(ImageFilter.MaxFilter(3))
    erosion = binarizada.filter(ImageFilter.MinFilter(3))
    gradiente = ImageChops.subtract(dilatacion, erosion)
    return gradiente
    
          
                    
                  
