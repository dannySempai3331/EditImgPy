import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from util.utilSys import getOS, getUsuario
from util.utilIcons import abrirIcono, ajustarIcono

from Funciones.hdr import genHdrImg

class VentanaHDR(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Generar imagen HDR")
        self.geometry("820x600")
        
        self.images = []
        self.paths = []
        
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.iconAbrir = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/upload_3720553.png"), 30, 30))
        
        self.add_button = tk.Button(self.top_frame, image=self.iconAbrir, command=self.add_image)
        self.add_button.pack(side=tk.LEFT)

        self.cancel_button = tk.Button(self.top_frame, text="Cancelar", command=self.cancel)
        self.cancel_button.pack(side=tk.RIGHT)
        
        self.accept_button = tk.Button(self.top_frame, text="Generar", command=self.accept,state="disabled")
        self.accept_button.pack(side=tk.RIGHT)

        self.canvas.bind("<Configure>", self.configure_scrollregion)

    def add_image(self):
        os = getOS()
        if os == "Linux":
            file_path = filedialog.askopenfilename(initialdir=getUsuario()+"/Documents/",title="Selecciona una imagen",filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
            if file_path:
                img = Image.open(file_path)
                self.paths.append(file_path)
                img = img.resize((130, 130))
                img_tk = ImageTk.PhotoImage(img)
                
                self.images.append(img_tk)
        
                self.display_images()
                self.verificarLongitud()
        elif os == "Windows":
            file_path = filedialog.askopenfilename(initialdir="C:/Users/",title="Selecciona una imagen",filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
            if file_path:
                img = Image.open(file_path)
                self.paths.append(file_path)
                img = img.resize((130, 130))
                img_tk = ImageTk.PhotoImage(img)
                
                self.images.append(img_tk)
        
                self.display_images()
                self.verificarLongitud()
        elif os == "Darwin":
            file_path = filedialog.askopenfilename(initialdir=getUsuario()+"/Documents/",title="Selecciona una imagen",filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
            if file_path:
                img = Image.open(file_path)
                self.paths.append(file_path)
                img = img.resize((130, 130))
                img_tk = ImageTk.PhotoImage(img)
                
                self.images.append(img_tk)
        
                self.display_images()
                self.verificarLongitud()
    
    def display_images(self):

        self.canvas.delete("all")

        images_per_row = 5
        padding = 50
        
        # Display all images in the list
        for idx, img in enumerate(self.images):
            row = idx // images_per_row
            col = idx % images_per_row
            x = padding + col * (100 + padding)
            y = padding + row * (100 + padding)
            self.canvas.create_image(x, y, anchor=tk.NW, image=img)

        self.configure_scrollregion()

    def verificarLongitud(self):
        if len(self.images) > 2:
            self.accept_button.config(state="normal")

    def configure_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def accept(self):
        self.destroy()
        imgHdr=genHdrImg(self.paths)
        if imgHdr != None:
            imgHdr.show()
    
    def cancel(self):
        self.images.clear()
        self.paths.clear()
        self.canvas.delete("all")
        self.destroy()