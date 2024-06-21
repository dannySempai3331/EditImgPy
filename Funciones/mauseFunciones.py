import time
from PIL import Image, ImageTk, ImageDraw, ImageSequence
import tkinter as tk
import numpy as np  
import random
import threading
from math import floor
"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

loading_gif = None
loading_gif_frames = []   
loading_gif_canvas_id = None 
coordenadasSeleccionadas = []
coordenadas_listas = False

# Función para manejar el evento de presionar el botón del mouse
def on_button_press(event, operacion):
    global inicio_x, inicio_y, blanco_rect, negro_rect, operacion_actual, img, coordenadas_listas

    inicio_x, inicio_y = event.x, event.y
    operacion_actual = operacion

    if operacion_actual == "removerImperfecciones" or operacion_actual == "removerRostros":
        img_x = int((inicio_x / canvas.winfo_width()) * img.width)
        img_y = int((inicio_y / canvas.winfo_height()) * img.height)
        coordenadasSeleccionadas.append((img_x, img_y))
        coordenadas_listas = True
        return

    blanco_rect = canvas.create_rectangle(inicio_x, inicio_y, inicio_x, inicio_y, outline='white', width=3)
    negro_rect = canvas.create_rectangle(inicio_x + 1, inicio_y + 1, inicio_x + 1, inicio_y + 1, outline='black', width=1)

# Función para manejar el evento de mover el mouse con el botón presionado
def on_move_press(event):
    act_x, act_y = event.x, event.y
    canvas.coords(blanco_rect, inicio_x, inicio_y, act_x, act_y)
    canvas.coords(negro_rect, inicio_x + 1, inicio_y + 1, act_x + 1, act_y + 1)

# Función para manejar el evento de soltar el botón del mouse
def on_button_release(event):
    global coordenadasSeleccionadas, img, blanco_rect, negro_rect, inicio_x, inicio_y, operacion_actual, canvas, coordenadas_listas
    final_x, final_y = event.x, event.y

    if final_x < inicio_x:
        inicio_x, final_x = final_x, inicio_x
    if final_y < inicio_y:
        inicio_y, final_y = final_y, inicio_y

    img_x1 = int((inicio_x / canvas.winfo_width()) * img.width)
    img_y1 = int((inicio_y / canvas.winfo_height()) * img.height)
    img_x2 = int((final_x / canvas.winfo_width()) * img.width)
    img_y2 = int((final_y / canvas.winfo_height()) * img.height)

    coordenadasSeleccionadas = [(img_x1, img_y1), (img_x2, img_y2)]

    canvas.delete(blanco_rect)
    canvas.delete(negro_rect)
    coordenadas_listas = True
 

def cambiarPixeles(orgImg, orgCanvas):
    global coordenadasSeleccionadas, canvas, img, coordenadas_listas,flag

    img = orgImg
    canvas = orgCanvas
    
    canvas.bind("<ButtonPress-1>", lambda event: on_button_press(event, "cambiarPixeles"))
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            unbind_mouse_events()
            return img

    C1 = coordenadasSeleccionadas[0]
    C2 = coordenadasSeleccionadas[1]
    draw = ImageDraw.Draw(img)

    for x in range(C1[0], C2[0]):
        for y in range(C1[1], C2[1]):
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            draw.point((x, y), (red, green, blue))

    coordenadasSeleccionadas.clear()
    coordenadas_listas = False
    return img
    
def limpieza(orgImg, orgCanvas):
    global coordenadasSeleccionadas, canvas, img, coordenadas_listas, flag

    img = orgImg
    canvas = orgCanvas
    
    canvas.bind("<ButtonPress-1>", lambda event: on_button_press(event, "limpieza"))
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            unbind_mouse_events()
            return img

    draw = ImageDraw.Draw(img)

    C1 = coordenadasSeleccionadas[0]
    C2 = coordenadasSeleccionadas[1]

    for x in range(C1[0], C2[0]):
        for y in range(C1[1], C2[1]):
            red = 0
            green = 0
            blue = 0
            draw.point((x, y), (red, green, blue))

    imgLimpia = img.copy()
    coordenadas_listas = False
    coordenadasSeleccionadas.clear()
    return imgLimpia

def copia(orgImg, orgCanvas):
    global coordenadasSeleccionadas, canvas, img, coordenadas_listas, flag

    img = orgImg
    canvas = orgCanvas

    canvas.bind("<ButtonPress-1>", lambda event: on_button_press(event, "copia"))
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            unbind_mouse_events()
            return img

    C1 = coordenadasSeleccionadas[0]
    C2 = coordenadasSeleccionadas[1]

    area = img.crop((C1[0],C1[1], C2[0], C2[1]))
    imgCopia = img.copy()
    imgCopia.paste(area)
    coordenadasSeleccionadas.clear()
    coordenadas_listas = False
    return imgCopia

def zoom(orgImg, orgCanvas):
    global coordenadasSeleccionadas, canvas, img, coordenadas_listas, flag

    img = orgImg
    canvas = orgCanvas

    canvas.bind("<ButtonPress-1>", lambda event: on_button_press(event, "zoom"))
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            unbind_mouse_events()
            return img

    imgZoom = img.copy()

    C1Origen = coordenadasSeleccionadas[0]
    C2Origen = coordenadasSeleccionadas[1]
    xOffset = C1Origen[0]
    yOffset = C1Origen[1]

    # Destino
    C1Destino = (0, 0)
    C2Destino = (imgZoom.width, imgZoom.height)

    # Calculo del Ratio
    xRatio = ((C2Origen[0] - C1Origen[0] + 1)) / C2Destino[0]
    yRatio = ((C2Origen[1] - C1Origen[1] + 1)) / C2Destino[1]

    # Crear nueva imagen
    nuevaImagen = Image.new('RGB', (C2Destino[0], C2Destino[1]))

    for x in range(C1Destino[0], C2Destino[0]):
        for y in range(C1Destino[1], C2Destino[1]):
            # Calculamos coorPrima
            CPrima = calculoDestino(x, y, xRatio, yRatio, xOffset, yOffset)
            # Asignamos el color al pixel x, y; según el color del pixel CPrima
            color = imgZoom.getpixel(CPrima)
            nuevaImagen.putpixel((x, y), color)

    coordenadasSeleccionadas.clear()
    coordenadas_listas = False
    return nuevaImagen

def calculoDestino(x, y, xRatio, yRatio, xOffset, yOffset):
    CPrima = (floor((x * xRatio) + xOffset), floor((y * yRatio) + yOffset))
    return CPrima

def distancia_euclidiana(p1, p2):
    return np.sqrt(((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))

def promedio_adyacentes(x, y, size,tipo):
    global img
    adyacentes = []
    if tipo == "imperfecciones":
        for i in range(-size-9, size + 10):
            for j in range(-size-9, size + 10):
                if (0 <= x + i < img.width) and (0 <= y + j < img.height):
                    adyacentes.append(img.getpixel((x + i, y + j)))
        return tuple(np.mean(adyacentes, axis=0).astype(int))
    else:
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                if (0 <= x + i < img.width) and (0 <= y + j < img.height):
                    adyacentes.append(img.getpixel((x + i, y + j)))
        return tuple(np.mean(adyacentes, axis=0).astype(int))

def reemplazar_vecinos(x, y, radio):
    for i in range(-radio, radio+1):
        for j in range(-radio, radio+1):
            if ((0 <= x+i < img.width) and (0 <= y+j < img.height)):
                distancia = distancia_euclidiana((x, y), (x+i, y+j))
                if distancia <= radio:
                    size = max(1, int(min(img.width, img.height) * 0.01))
                    nuevo_color = promedio_adyacentes(x+i, y+j, size,"Rostro")
                    img.putpixel((x+i, y+j), nuevo_color)
    
def eliminarRostros(orgImg, orgCanvas, orgRadio, root):
    global img, canvas, radio, coordenadas_listas, coordenadasSeleccionadas,flag
    img = orgImg
    canvas = orgCanvas
    radio = orgRadio
    
    canvas.bind("<Button-1>", lambda event: on_button_press(event, "removerRostros"))
    
    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            return img
    
    C1 = coordenadasSeleccionadas[0]
    
    # Mostrar GIF de carga
    cargar_gif(root)

    # Crear un hilo para el procesamiento
    thread = threading.Thread(target=eliminarRostros_proceso, args=(C1, radio))
    thread.start()
    thread.join()  # Esperar a que el hilo termine

    # Ocultar GIF de carga
    ocultar_gif()
    coordenadasSeleccionadas.clear()  
    coordenadas_listas = False
    return img

def eliminarRostros_proceso(C1, radio):
    # Aplicar el algoritmo de reemplazo de vecinos
    for _ in range(3):
        reemplazar_vecinos(C1[0], C1[1], radio)
    return img

def cargar_gif(root):
    global loading_gif, loading_gif_frames, loading_gif_canvas_id
    blanco = Image.new('RGB', (100, 100), color='white')
    mostrar_imagen(blanco)
    loading_gif = Image.open("icons/loading.gif")
    loading_gif_frames = [ImageTk.PhotoImage(frame.copy().resize((canvas.winfo_width(), canvas.winfo_height()))) for frame in ImageSequence.Iterator(loading_gif)]
    if loading_gif_canvas_id is None:
        loading_gif_canvas_id = canvas.create_image(0, 0, anchor=tk.NW, image=loading_gif_frames[0])
    root.after(0, actualizar_gif, 0, root)

def actualizar_gif(frame, root):
    global loading_gif_canvas_id
    if loading_gif_canvas_id:
        frame %= len(loading_gif_frames)
        canvas.itemconfig(loading_gif_canvas_id, image=loading_gif_frames[frame])
        root.after(100, actualizar_gif, frame + 1, root)


def ocultar_gif():
    global loading_gif_canvas_id
    if loading_gif_canvas_id:
        canvas.delete(loading_gif_canvas_id)
        loading_gif_canvas_id = None

def mostrar_imagen(imagen):
    tkImg = ImageTk.PhotoImage(imagen.resize((canvas.winfo_width(), canvas.winfo_height())))
    canvas.create_image(0, 0, anchor=tk.NW, image=tkImg)
    canvas.image_ref = tkImg

def removerImperfecciones(orgImg,orgCanvas):
    global coordenadasSeleccionadas, canvas, img, coordenadas_listas, flag

    img = orgImg
    canvas = orgCanvas
    
    canvas.bind("<ButtonPress-1>", lambda event: on_button_press(event, "removerImperfecciones"))

    while not coordenadas_listas:
        canvas.update()
        time.sleep(0.1)
        if flag == False:
            return img
    
    C1 = coordenadasSeleccionadas[0]

    size = max(1, int(min(img.width, img.height) * 0.01))
    color_promedio = promedio_adyacentes(C1[0], C1[1], size,"imperfecciones")
    
    # Cambiar la región de píxeles 
    for i in range(-size, size+1):
        for j in range(-size, size+1):
            x = C1[0] + i
            y = C1[1] + j
            if ((0 <= x < img.width) and (0 <= y < img.height)):
                img.putpixel((x, y), color_promedio)
                
    imgImperfecciones = img.copy()
    coordenadasSeleccionadas.clear()  
    coordenadas_listas = False
    return imgImperfecciones

def banderaClick(orgFlag):
    global flag
    flag = orgFlag

def unbind_mouse_events():
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
