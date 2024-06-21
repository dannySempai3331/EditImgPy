from PIL import Image

def abrirIcono(iconPath):
    icon = Image.open(iconPath)
    return icon

def ajustarIcono(icon, ancho, alto):
    icon = icon.resize((ancho, alto))
    return icon
    