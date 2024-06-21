from PIL import Image, ImageTk
from tkinter import filedialog
from util.utilSys import getOS, getUsuario, getFechaHora
import matplotlib.pyplot as plt
from io import BytesIO
from Funciones.huffman import descomprimir

def cargarImagen():
    os = getOS()
    if os == "Linux":
        dirUsuario = getUsuario()
        textFile = filedialog.askopenfilename(initialdir=dirUsuario+"/Documents/", title="Selecciona una imagen", filetypes=((("Archivos de imagen", "*.jpg"),("Archivos de imagen", "*.jpeg") , ("Archivos de imagen", "*.png"), ("Archivos de imagen", "*.huff"))))
    elif os == "Windows":
        textFile = filedialog.askopenfilename(initialdir="C:/Users/", title="Selecciona una imagen", filetypes=((("Archivos de imagen", "*.jpg"),("Archivos de imagen", "*.jpeg") , ("Archivos de imagen", "*.png"), ("Archivos de imagen", "*.huff"))))    
    elif os == "Darwin":
        dirUsuario = getUsuario()
        textFile = filedialog.askopenfilename(initialdir=dirUsuario+"/Documents/", title="Selecciona una imagen", filetypes=((("Archivos de imagen", "*.jpg"),("Archivos de imagen", "*.jpeg") , ("Archivos de imagen", "*.png"), ("Archivos de imagen", "*.huff"))))
    
    if obtenerExtension(textFile) == "huff":
        imgD = descomprimir(textFile)
        return imgD
    image = Image.open(textFile)
    return image

def guardarImagen(img):
    os = getOS()

    if os == "Linux":
        directorio = filedialog.askdirectory(initialdir=getUsuario()+"/Documents/", title="Guardar imagen")
        if directorio:
            filename = getFechaHora()+"_pid"+".png"
            file_path = f"{directorio}/{filename}"
            img.save(file_path)
    elif os == "Windows":
        directorio = filedialog.askdirectory(initialdir="C:/Users/", title="Guardar imagen")
        if directorio:
            filename = getFechaHora()+"_pid"+".png"
            file_path = f"{directorio}/{filename}"
            img.save(file_path)
    elif os == "Darwin":
        directorio = filedialog.askdirectory(initialdir=getUsuario()+"/Documents/", title="Guardar imagen")
        if directorio:
            filename = getFechaHora()+"_pid"+".png"
            file_path = f"{directorio}/{filename}"
            img.save(file_path)        

def redimensionarImg(img,nwidth,nheight):
    return img.resize((nwidth,nheight))

def getProfundidadColor(image):
    with image as img:

        modeToDepth={
            "1":1,
            "L":8,
            "P":8,
            "RGB":24,
            "RGBA":32,
            "CMYK":32,
            "YCbCr":24,
            "LAB":24,
            "HSV":24,
            "I":32,
            "F":32
        }
        bitDepth = modeToDepth.get(img.mode,"Desconocido")
        return bitDepth
    
def getPesoImg(img):
    #print(img.format)
    try:
        output = BytesIO()
        img.save(output, format=img.format)
        size = output.tell()
        size = size/(1024*1024)
        return size
    except ValueError as e:
        print(f"Error al obtener el formato de la imagen: {e}")
        return 0.0  
    
def calcularHistorgrama(img):
    if estaAColor(img):
    
        imgH = img.histogram()
        fig, ax = plt.subplots()
        ax.plot(imgH[0:256], color='red', label='Rojo')
        ax.plot(imgH[256:512], color='green', label='Verde')
        ax.plot(imgH[512:768], color='blue', label='Azul')
        ax.legend()
        ax.set_title('Histograma de la imagen')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        fig.tight_layout()
        return fig
    else:
        imgH = img.histogram()

        fig, ax = plt.subplots()
        ax.plot(imgH[0:256], color='black')
        #ax.legend()
        ax.set_title('Histograma de la imagen')
        ax.set_xlabel('Intensidad de píxeles')
        ax.set_ylabel('Frecuencia')
        fig.tight_layout()
        return fig
    
def estaAColor(img):
    img = img.convert('RGB')
    pixeles = img.getdata()
    for pixel in pixeles:
        r, g, b = pixel
        if r != g or g != b:
            return True
    return False

def obtenerExtension(archivo):
    partes = archivo.split('.')
    if len(partes) > 1:
        return partes[-1]
    else:
        return ''







    

