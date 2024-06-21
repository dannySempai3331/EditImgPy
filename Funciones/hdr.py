from PIL import Image
from tkinter import messagebox
import numpy as np

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

imgHdr = None

def genHdrImg(listaPaths):
    global imgHdr
    #abrir las imagenes y colocarlas en una lista
    listaImg = [Image.open(path) for path in listaPaths]
    #verificar que las imagenes sean del mismo tamaño
    if verificarTamanio(listaImg):
        stacked_images = np.stack(listaImg, axis=0)
        hdr_image = np.mean(stacked_images, axis=0)
        hdr_image = np.clip(hdr_image, 0, 255)   
        imgHdr = Image.fromarray(hdr_image.astype('uint8'))

def verificarTamanio(listaImg):
    ancho, alto = listaImg[0].size

    for img in listaImg:

        anchoActual, altoActual = img.size
        if anchoActual != ancho or altoActual != alto:
            messagebox.showinfo("Error", "Las imagenes deben ser del mismo tamaño")
            return False
    return True

def returnImgHdr():
    return imgHdr
