import time
from PIL import Image, ImageDraw, ImageTk
from tkinter import messagebox
import numpy as np

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

coordenadasSeleccionadas = []

def pintarConRegion(event, size):
    global regionGuardada, imgCopy, image_width, image_height, canvas_width, canvas_height, coordenadas_listas

    if not regionGuardada:
        messagebox.showinfo("Mensaje", "Selecciona una región primero con el clic derecho")
        return

    draw = ImageDraw.Draw(imgCopy)
    x, y = event.x, event.y
    img_x = int((x / canvas_width) * image_width)
    img_y = int((y / canvas_height) * image_height)

    radio = size
    
    # Crear un diccionario para acceso más rápido a los colores de la región guardada
    coloresRegion = {(i, j): np.array(color) for i, j, color in regionGuardada}

    for dx in range(-radio, radio + 1):
        for dy in range(-radio, radio + 1):
            distancia = np.sqrt(dx**2 + dy**2)
            if distancia <= radio:
                xi = img_x + dx
                yj = img_y + dy
                if 0 <= xi < image_width and 0 <= yj < image_height:
                    # Cuánto se mezclarán los colores de acuerdo a la distancia
                    mezcla = 1 - (distancia / radio)
                    # Color de la imagen original
                    colorOriginal = np.array(imgCopy.getpixel((xi, yj)))
                    # Color de la región guardada
                    colorRegion = coloresRegion.get((dx, dy), colorOriginal)
                    # Se mezclan ambos colores para que sea más suave
                    mezclaColor = (mezcla * colorRegion + (1 - mezcla) * colorOriginal).astype(int)
                    draw.point((xi, yj), tuple(mezclaColor))

    coordenadas_listas = True  # Indicar que se han pintado las coordenadas
    return imgCopy

def seleccionarRegion(event, size, label):
    global regionGuardada, imgCopy, image_width, image_height
    
    x, y = event.x, event.y
    img_x = int((x / canvas_width) * image_width)
    img_y = int((y / canvas_height) * image_height)
    regionGuardada = []
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            xi = img_x + i
            yj = img_y + j
            if 0 <= xi < image_width and 0 <= yj < image_height:
                regionGuardada.append((i, j, imgCopy.getpixel((xi, yj))))

    # Mostrar la región seleccionada en el label
    if regionGuardada:
        region_img = Image.new('RGB', (2*size + 1, 2*size + 1))
        for i, j, color in regionGuardada:
            region_img.putpixel((i + size, j + size), color)
        region_img_tk = ImageTk.PhotoImage(region_img)
        label.config(image=region_img_tk)
        label.image = region_img_tk

def removerObjetos(orgImg, orgCanvas, orgSize, label):
    global regionGuardada, image_width, image_height, root, img, canvas_width, canvas_height, imgCopy, coordenadas_listas, flag
    
    img = orgImg
    canvas = orgCanvas
    size = orgSize

    image_width, image_height = img.size
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    imgCopy = img.copy()
    coordenadas_listas = False  

    def seleccionarRegionWrapper(event):
        seleccionarRegion(event, size, label)
        
    def pintarConRegionWrapper(event):
        pintarConRegion(event, size)

    canvas.bind("<Button-1>", pintarConRegionWrapper)
    canvas.bind("<Button-3>", seleccionarRegionWrapper)

    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            return img

    return imgCopy

def banderaObjeto(orgFlag):
    global flag
    flag = orgFlag
