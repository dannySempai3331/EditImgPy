import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageEnhance, ImageFilter
import math

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

offset = 10

def brillo(img,brillo):
    return ImageEnhance.Brightness(img).enhance(brillo)

def contraste(img,contraste):
    return ImageEnhance.Contrast(img).enhance(contraste)

def rotar90(img):
    return img.rotate(-90,expand=True) 
    
def rotarMenos90(img):
    return img.rotate(90,expand=True)

def espejoHorizontal(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)
    
def espejoVertical(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)

def desplazamientoUp(img):
    global offset

    return img.crop((0, offset, img.width, img.height + offset))
 
def desplazamientoDown(img):
    global offset

    return img.crop((0, -offset, img.width, img.height - offset))
    
def desplazamientoLeft(img):
    global offset

    return img.crop((offset, 0, img.width + offset, img.height))

def desplazamientoRight(img):
    global offset

    return img.crop((-offset, 0, img.width - offset, img.height))
    
def intensityLevelSlicing (img,umbral1, umbral2):
    return img.point(lambda x: 255 if umbral1 <= x <= umbral2 else 0)
    
def transformacionLog(img, c):
    return img.point(lambda x: c * math.log(1 + x, 2) / math.log(256, 2))
    
#Transformación de potencia:
def transformacionPot(img,c,y):
    return img.point(lambda x: c * (x / 255) ** y)

 
