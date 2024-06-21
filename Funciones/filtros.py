from PIL import ImageFilter

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

def desenfoque(img):
    imgDesenfocada = img.filter(ImageFilter.GaussianBlur(4))
    return imgDesenfocada

def detalle(img):
    imgDetallada = img.filter(ImageFilter.DETAIL)
    return imgDetallada

def suavizado(img):
    imgSuave = img.filter(ImageFilter.SMOOTH)
    return imgSuave

def nitidez(img):
    imgNitida = img.filter(ImageFilter.SHARPEN)
    return imgNitida

#Relieve
def relieve(img):
    imgRel = img.filter(ImageFilter.EMBOSS)
    return imgRel

#Resaltar Bordes
def resaltarBordes(img):
    imgRB = img.filter(ImageFilter.CONTOUR)
    return imgRB

#Realzar Bordes
def realzarBordes(img):
    imgReB = img.filter(ImageFilter.EDGE_ENHANCE)
    return imgReB

#Detectar Bordes
def detectarBordes(img):
    imgDB = img.filter(ImageFilter.FIND_EDGES)
    return imgDB
