import tkinter as tk
from PIL import Image, ImageOps
from util.utilImg import estaAColor

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

def sepiaCalido(img):
    anchura, altura = img.size
    imagenSepiaCalido = Image.new("RGB", (anchura, altura))
    
    for x in range(anchura):
        for y in range(altura):
            r, g, b = img.getpixel((x, y))
            tono_sepia_r = int(0.393 * r + 0.769 * g + 0.189 * b)
            tono_sepia_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            tono_sepia_b = int(0.272 * r + 0.534 * g + 0.131 * b)
            imagenSepiaCalido.putpixel((x, y), (tono_sepia_r, tono_sepia_g, tono_sepia_b))

    return imagenSepiaCalido

def sepiaFrio(img):
    anchura, altura = img.size
    imagenSepiaFrio = Image.new("RGB", (anchura, altura))
    
    for x in range(anchura):
        for y in range(altura):
            r, g, b = img.getpixel((x, y))
            tono_sepia_r = int(0.272 * r + 0.534 * g + 0.131 * b)
            tono_sepia_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            tono_sepia_b = int(0.272 * r + 0.534 * g + 0.131 * b)
            imagenSepiaFrio.putpixel((x, y), (tono_sepia_r, tono_sepia_g, tono_sepia_b))
    
    return imagenSepiaFrio

def sepiaVintage(img):
    anchura, altura = img.size
    imagenSepiaV = Image.new("RGB", (anchura, altura))
    
    for x in range(anchura):
        for y in range(altura):
            r, g, b = img.getpixel((x, y))
            tono_sepia_r = int(0.45 * r + 0.75 * g + 0.2 * b)
            tono_sepia_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            tono_sepia_b = int(0.272 * r + 0.534 * g + 0.131 * b)
            imagenSepiaV.putpixel((x, y), (tono_sepia_r, tono_sepia_g, tono_sepia_b))
    
    return imagenSepiaV

def sepiaIntenso(img):
    anchura, altura = img.size
    imagenSepiaI = Image.new("RGB", (anchura, altura))
    
    for x in range(anchura):
        for y in range(altura):
            r, g, b = img.getpixel((x, y))
            tono_sepia_r = int(0.5 * r + 0.6 * g + 0.4 * b)
            tono_sepia_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            tono_sepia_b = int(0.272 * r + 0.534 * g + 0.131 * b)
            imagenSepiaI.putpixel((x, y), (tono_sepia_r, tono_sepia_g, tono_sepia_b))
    
    return imagenSepiaI

def sepiaSuave(img):
    anchura, altura = img.size
    imagenSepiaS = Image.new("RGB", (anchura, altura))
    
    for x in range(anchura):
        for y in range(altura):
            r, g, b = img.getpixel((x, y))
            tono_sepia_r = int(0.35 * r + 0.65 * g + 0.15 * b)
            tono_sepia_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            tono_sepia_b = int(0.272 * r + 0.534 * g + 0.131 * b)
            imagenSepiaS.putpixel((x, y), (tono_sepia_r, tono_sepia_g, tono_sepia_b))
    
    return imagenSepiaS

def escalaGrises(img):
    
    if estaAColor(img):
        img = img.convert('L')

    return img

def inversion(img):
    imgNegativa = ImageOps.invert(img)
    return imgNegativa

    
    
