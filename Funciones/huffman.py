from PIL import Image
from collections import defaultdict, Counter
from util.utilSys import getFechaHora, getOS, getUsuario
from tkinter import filedialog
import heapq
import pickle

class Nodo:
    def __init__(self, frequency, color, left=None, right=None):
        self.frequency = frequency
        self.color = color
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency
    
def construirArbol(frecuencias):
    heap = [Nodo(freq, color) for color, freq in frecuencias.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        izq = heapq.heappop(heap)
        der = heapq.heappop(heap)
        merged = Nodo(izq.frequency + der.frequency, None, izq, der)
        heapq.heappush(heap, merged)
    return heap[0]

def generarCodigos(nodo, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if nodo.color is not None:
        codebook[nodo.color] = prefix
    else:
        generarCodigos(nodo.left, prefix + "0", codebook)
        generarCodigos(nodo.right, prefix + "1", codebook)
    return codebook

def comprimir(image):
    pixels = list(image.getdata())
    frequencies = Counter(pixels)
    huffman_tree = construirArbol(frequencies)

    huffman_codes = generarCodigos(huffman_tree)
    encoded_image = ''.join(huffman_codes[pixel] for pixel in pixels)
    
    extra_padding = 8 - len(encoded_image) % 8
    for i in range(extra_padding):
        encoded_image += "0"
    
    encoded_image_bytes = bytearray()
    for i in range(0, len(encoded_image), 8):
        byte = encoded_image[i:i+8]
        encoded_image_bytes.append(int(byte, 2))
    
    with open(guardarImagen() + ".huff", "wb") as f:
        pickle.dump((encoded_image_bytes, huffman_codes, extra_padding, image.size, image.mode), f)

def descomprimir(compressed_file_path):
    with open(compressed_file_path, "rb") as f:
        encoded_image_bytes, huffman_codes, extra_padding, image_size, image_mode = pickle.load(f)
    
    encoded_image = ''.join(format(byte, '08b') for byte in encoded_image_bytes)
    encoded_image = encoded_image[:-extra_padding]
    
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    
    current_code = ""
    decoded_pixels = []
    for bit in encoded_image:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_pixels.append(reverse_huffman_codes[current_code])
            current_code = ""
    
    new_image = Image.new(image_mode, image_size)
    new_image.putdata(decoded_pixels)
    
    return new_image

def guardarImagen():
    os = getOS()
    if os == "Linux":
        directorio = filedialog.askdirectory(initialdir=getUsuario()+"/Documents/", title="Guardar imagen")
        if directorio:
            filename = getFechaHora()+"_pid"
            file_path = f"{directorio}/{filename}"
            return file_path
            
    elif os == "Windows":
        directorio = filedialog.askdirectory(initialdir="C:/Users/", title="Guardar imagen")
        if directorio:
            filename = getFechaHora()+"_pid"
            file_path = f"{directorio}/{filename}"
            return file_path
    elif os == "Darwin":
        directorio = filedialog.askdirectory(initialdir=getUsuario()+"/Documents/", title="Guardar imagen")
        if directorio:
            filename = getFechaHora()+"_pid"
            file_path = f"{directorio}/{filename}"
            return file_path
           