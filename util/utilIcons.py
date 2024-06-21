from PIL import Image

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

def abrirIcono(iconPath):
    icon = Image.open(iconPath)
    return icon

def ajustarIcono(icon, ancho, alto):
    icon = icon.resize((ancho, alto))
    return icon
    
