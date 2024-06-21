from PIL import ImageOps, Image
from util.utilImg import estaAColor
import numpy as np

def ecualizar(img):
    imgEc = ImageOps.equalize(img)
    return imgEc

def comprimir(pixel_value, min_value, max_value, smin, smax):
    c = int(((smax-smin)/(max_value-min_value))*(pixel_value-min_value)+smin)
    if c > 255:
        return 255
    return c

def compresion(img,sm,sM):
    img = img.convert("L")
    valores_pixeles = list(img.getdata())
    v_min = min(valores_pixeles)
    v_max = max(valores_pixeles)
    imgComprimida = Image.new("L", img.size)
    imgComprimida.putdata([comprimir(p, v_min, v_max,int(sm),int(sM)) for p in valores_pixeles])
    return imgComprimida

def desplazar(pixel, v_desplazamiento):
    p = pixel + v_desplazamiento
    if p < 0:
        return 0
    elif p > 255:
        return 255
    
    return p

def desplazamiento(img, v_desplazamiento):
    img = img.convert("L")
    valores_pixeles = list(img.getdata())

    imgDesplazada = Image.new("L", img.size)
    imgDesplazada.putdata([desplazar(p, v_desplazamiento) for p in valores_pixeles])

    return imgDesplazada

def expansionLineal(pixel_value, min_value, max_value):

    lx = int(255 * ((pixel_value - min_value) / (max_value - min_value)))

    if lx > 255:
        return 255
    
    return lx

def expanL(img):
    img = img.convert("L")
    valores_pixeles = list(img.getdata())

    v_min = min(valores_pixeles)
    v_max = max(valores_pixeles)

    imagen_expandida = img.point(lambda p: expansionLineal(p, v_min, v_max))

    return imagen_expandida

def umbralizar(pixel, umbral):
    if pixel < umbral:
        return 0
    elif pixel >= umbral:
        return 255
    
def thresholding(img):
    img = img.convert("L")
    imgHistograma = img.histogram()
    sum_ocurrencias = sum(imgHistograma)
    sum_total = 0

    for intensidad, ocurrencias in enumerate(imgHistograma):
        sum_total += intensidad * ocurrencias

    media = int(sum_total / sum_ocurrencias)

    imgUmbralizada = Image.new('L', img.size)
    imgUmbralizada.putdata([umbralizar(p, media) for p in img.getdata()])

    return imgUmbralizada

    
    