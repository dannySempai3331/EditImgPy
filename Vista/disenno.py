import tkinter as tk
from tkinter import font, PhotoImage
import matplotlib.pyplot as plt
from config import COLOR_BARRA_SUPERIOR, COLOR_BARRA_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.utilVentana as uVentana
import util.utilImg as uImg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from util.utilIcons import abrirIcono, ajustarIcono
from Funciones.color import *
from Funciones.filtros import *
from Funciones.editor import *
from Funciones.hdr import returnImgHdr
from Funciones.histograma import *
from Funciones.mauseFunciones import limpieza, copia, zoom, cambiarPixeles, removerImperfecciones, eliminarRostros, banderaClick
from Funciones.morfologia import *
from Funciones.retoque import *
from Funciones.huffman import comprimir
from Vista.HDR import VentanaHDR
import threading

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

class Principal(tk.Tk):

    primeraCarga = False
    listaImagenes = []
    contadorImagenes = -1

    def __init__(self):
        super().__init__()

        self.configVentana()
        self.configPaneles()
        self.controlBarraSup()
        self.controlMenuLateral()
        self.configurarBarraInf()
        self.configurarCuerpoPrincipal()
        self.configurarFrameHistograma()
        self.configurarFrameOpHistograma()
        self.configurarSubMenuEditar()
        self.configurarSubMenuColor()
        self.configurarSubMenuFitros()
        self.configurarSubMenuRetoque()
        self.configurarSubMenuMorfologia()

    def dimensionesPantalla(self):
        return self.winfo_screenwidth(), self.winfo_screenheight()

    def configVentana(self):
        self.title("EditImgPy")
        w,h = self.dimensionesPantalla()
        uVentana.centrarVentana(self,w,h)

    def configPaneles(self):
        self.barraSuperior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=40)
        self.barraSuperior.pack(side= tk.TOP, fill='both')

        self.barraInf = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=30)
        self.barraInf.pack(side= tk.BOTTOM, fill='both')

        self.menuLateral = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, width=150)
        self.menuLateral.pack(side= tk.LEFT, fill='both', expand=False)

        self.subMenuEditar = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=230)

        self.subMenuColor = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=230)

        self.subMenuFiltros = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=230)

        self.subMenuRetoque = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=230)

        self.subMenuMorfologia = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=230)
        
        self.frameHistograma = tk.Frame(self, bg=COLOR_BARRA_LATERAL, width=550)
        self.frameHistograma.pack(side= tk.RIGHT,fill='both')

        self.cuerpoPrincipal = tk.Frame(self, bg="lightgrey")
        self.cuerpoPrincipal.pack(side= tk.RIGHT, fill='both', expand=True)

        
    def controlBarraSup(self):

        fontAwesome = font.Font(family='FontAwesome', size=13)

        self.titulo = tk.Label(self.barraSuperior, text="Menu")
        self.titulo.config(fg='#fff', font=("Roboto",12), bg=COLOR_BARRA_SUPERIOR, pady=10,width=7)
        self.titulo.pack(side=tk.LEFT)

        self.separador1 = tk.Frame(self.barraSuperior, bg=COLOR_BARRA_SUPERIOR, width=10)
        self.separador1.pack(side=tk.LEFT, fill='x', expand=True)

        self.iconAbrir = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/upload_3720553.png"), 30, 30))
    
        self.botonAbrir = tk.Button(self.barraSuperior, image=self.iconAbrir, font=fontAwesome,command=self.colocarImgCanvas ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white")
        self.botonAbrir.pack(side=tk.LEFT)

        self.iconGuardar = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/floppy-disk_1191252.png"), 30, 30))

        self.botonGuardar = tk.Button(self.barraSuperior, image=self.iconGuardar, font=fontAwesome,command=lambda:uImg.guardarImagen(self.img) ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white",state="disabled")
        self.botonGuardar.pack(side=tk.LEFT,padx=10)

        self.iconHuff = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/zip_7039807.png"), 30, 30))

        self.botonHuff = tk.Button(self.barraSuperior, image=self.iconHuff,command=lambda:comprimir(self.img) ,font=fontAwesome ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white",state="disabled")
        self.botonHuff.pack(side=tk.LEFT)

        self.iconHist = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/graphic_2223954.png"), 30, 30))

        self.botonHist = tk.Button(self.barraSuperior, image=self.iconHist, font=fontAwesome,command=self.toggleHistograma ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white")
        self.botonHist.pack(side=tk.RIGHT,padx=10)

        self.iconClean = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/broom_4652225.png"), 30, 30))

        self.botonClean = tk.Button(self.barraSuperior, image=self.iconClean, font=fontAwesome,command=self.limpiar ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white",state="disabled")
        self.botonClean.pack(side=tk.RIGHT)

        self.botonHist = tk.Button(self.barraSuperior, text="Hist", font=fontAwesome, bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white")

        self.botonReDo = tk.Button(self.barraSuperior, text="↻", font=fontAwesome,command=self.reDo ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white",state="disabled")
        self.botonReDo.pack(side=tk.RIGHT)

        self.botonUnDo = tk.Button(self.barraSuperior, text="↺", font=fontAwesome,command=self.unDo ,bd=0, bg= COLOR_BARRA_SUPERIOR, fg="white",state="disabled")
        self.botonUnDo.pack(side=tk.RIGHT)

        self.separador2 = tk.Frame(self.barraSuperior, bg=COLOR_BARRA_SUPERIOR, width=10)
        self.separador2.pack(side=tk.RIGHT, fill='x', expand=True)
        
    def controlMenuLateral(self):

        self.editarIcon = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/paint-brush_232352.png"), 50, 50))
        self.colorIcon = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/color-palette_3854709.png"), 50, 50))
        self.filtrosIcon = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/settings_262601.png"), 50, 50))
        self.retoqueIcon = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/brushes_2872680.png"), 50, 50))
        self.mofIcon = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/cube_6936983.png"), 50, 50))
        self.hdrIcon = ImageTk.PhotoImage(ajustarIcono(abrirIcono("icons/gallery_4898355.png"), 50, 50))
        
        self.botonEditar = tk.Button(self.menuLateral,image=self.editarIcon,bg=COLOR_BARRA_LATERAL,state= "disabled")
        self.botonColor = tk.Button(self.menuLateral,image=self.colorIcon,bg=COLOR_BARRA_LATERAL, state= "disabled")
        self.botonFiltros = tk.Button(self.menuLateral,image=self.filtrosIcon,bg=COLOR_BARRA_LATERAL,state= "disabled")
        self.botonRetoque = tk.Button(self.menuLateral,image=self.retoqueIcon,bg=COLOR_BARRA_LATERAL,state= "disabled")
        self.botonMas = tk.Button(self.menuLateral,image=self.mofIcon,bg=COLOR_BARRA_LATERAL,state= "disabled")
        self.botonHdr = tk.Button(self.menuLateral,image=self.hdrIcon,bg=COLOR_BARRA_LATERAL)

        self.botonEditar.pack(side=tk.TOP)
        self.botonColor.pack(side=tk.TOP)
        self.botonFiltros.pack(side=tk.TOP)
        self.botonRetoque.pack(side=tk.TOP)
        self.botonMas.pack(side=tk.TOP)
        self.botonHdr.pack(side=tk.TOP)

        self.bindHoverEvent(self.botonEditar)
        self.bindHoverEvent(self.botonColor)
        self.bindHoverEvent(self.botonFiltros)
        self.bindHoverEvent(self.botonRetoque)
        self.bindHoverEvent(self.botonMas)
        self.bindHoverEvent(self.botonHdr)

        self.botonEditar.config(command=self.toggleSubMenuEditar)
        self.botonColor.config(command=self.toggleSubMenuColor)
        self.botonFiltros.config(command=self.toggleSubMenuFiltros)
        self.botonRetoque.config(command=self.toggleSubMenuRetoque)
        self.botonMas.config(command=self.toggleSubMenuMorfologia)
        self.botonHdr.config(command=self.generarHdr)

    def bindHoverEvent(self, boton):
        boton.bind("<Enter>", lambda event: self.on_enter(event, boton))
        boton.bind("<Leave>", lambda event: self.on_leave(event, boton))

    def on_enter(self, event, boton):
        boton.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg="white")

    def on_leave(self, event, boton):
        boton.config(bg=COLOR_BARRA_LATERAL, fg="white")

    def configurarCuerpoPrincipal(self):
        self.canvasCuerpo = tk.Canvas(self.cuerpoPrincipal, bg="lightgrey", width=50, height=50)
        self.canvasCuerpo.pack(side=tk.LEFT, expand=True)

        #agregar un icono
        icono = abrirIcono("icons/icons8-foto-64.png")
        icono = ajustarIcono(icono, 50, 50)
        photo = uImg.ImageTk.PhotoImage(icono)

        self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
        self.canvasCuerpo.image_ref = photo

        self.scrollbarCuerpoY = tk.Scrollbar(self.cuerpoPrincipal, orient=tk.VERTICAL, command=self.canvasCuerpo.yview)
        self.scrollbarCuerpoY.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvasCuerpo.config(yscrollcommand=self.scrollbarCuerpoY.set)

        self.canvasCuerpo.bind("<Configure>", self.configure_scrollregion)


    def configure_scrollregion(self, event=None):
        self.canvasCuerpo.configure(scrollregion=self.canvasCuerpo.bbox("all"))

    def configurarBarraInf(self):
        self.labelDimensiones = tk.Label(self.barraInf, text="Dim")
        self.labelDimensiones.config(fg='#fff', font=("Roboto",9), bg=COLOR_BARRA_SUPERIOR, pady=10,width=20)
        self.labelDimensiones.pack(side=tk.LEFT)

        self.labelProfundidad = tk.Label(self.barraInf, text="Prof. bits ")
        self.labelProfundidad.config(fg='#fff', font=("Roboto",9), bg=COLOR_BARRA_SUPERIOR, pady=10,width=20)
        self.labelProfundidad.pack(side=tk.LEFT)

        self.labelTamanio = tk.Label(self.barraInf, text="Tamaño ")
        self.labelTamanio.config(fg='#fff', font=("Roboto",9), bg=COLOR_BARRA_SUPERIOR, pady=10,width=20)
        self.labelTamanio.pack(side=tk.LEFT)

        self.separador3 = tk.Frame(self.barraInf, bg=COLOR_BARRA_SUPERIOR, width=375)
        self.separador3.pack(side=tk.LEFT, fill='x')

    def configurarFrameHistograma(self):
        self.iconH = abrirIcono("icons/analytics_15133269.png")

        fig, ax = plt.subplots()
    
        # Ocultar los ejes
        ax.axis('off')
        
        # Insertar la imagen en la figura
        ax.imshow(self.iconH)

        self.canvasHistograma = FigureCanvasTkAgg(master=self.frameHistograma ,figure=fig)
        self.canvasHistograma.get_tk_widget().config(width=550, height=400)
        self.canvasHistograma.get_tk_widget().pack(side=tk.TOP)
        self.canvasHistograma.draw()

        self.labelOpHistograma = tk.Label(self.frameHistograma, text="Operaciones con Histograma")
        self.labelOpHistograma.config(fg='#fff', font=("Roboto",12), bg=COLOR_BARRA_LATERAL, pady=10,width=30)
        self.labelOpHistograma.pack(side=tk.TOP)

        self.frameOpHistograma = tk.Frame(self.frameHistograma, bg=COLOR_BARRA_LATERAL)
        self.frameOpHistograma.pack(side=tk.TOP, fill='both',expand=True)

    def configurarFrameOpHistograma(self):

        self.labelCompresion = tk.Label(self.frameOpHistograma, text="Compresion")
        self.labelCompresion.config(fg='#fff', font=("Roboto",11), bg=COLOR_BARRA_LATERAL, pady=10,width=20)
        self.labelCompresion.grid(row=2, column=1, pady=5)

        self.labelDespH = tk.Label(self.frameOpHistograma, text="Desplazamiento")
        self.labelDespH.config(fg='#fff', font=("Roboto",11), bg=COLOR_BARRA_LATERAL, pady=10,width=20)
        self.labelDespH.grid(row=3, column=1, pady=5)

        self.botonEcualizar = tk.Button(self.frameOpHistograma, text="Ecualizar",command=lambda: self.actualizarImgCanvas(ecualizar(self.img)),bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=12,state="disabled")
        self.botonEcualizar.grid(row=4, column=2, pady=15)
        
        self.botonExpL = tk.Button(self.frameOpHistograma, text="Expansión L.",command=lambda: self.actualizarImgCanvas(expanL(self.img)),bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=12,state="disabled")
        self.botonExpL.grid(row=5, column=2, pady=15)

        self.botonThreshold = tk.Button(self.frameOpHistograma, text="Threshold",command=lambda: self.actualizarImgCanvas(thresholding(self.img)),bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=12,state="disabled")
        self.botonThreshold.grid(row=6, column=2, pady=15)

        self.labelMinComp = tk.Label(self.frameOpHistograma, text="Min")
        self.labelMinComp.config(fg='#fff', font=("Roboto",11), bg=COLOR_BARRA_LATERAL, pady=10,width=5)
        self.labelMinComp.grid(row=2, column=2, pady=5)

        self.spinnerCompresion1 = tk.Spinbox(self.frameOpHistograma, from_=0, to=255, width=5,state="disabled")
        self.spinnerCompresion1.grid(row=2, column=3, pady=5,padx=10)

        self.labelMaxComp = tk.Label(self.frameOpHistograma, text="Max")
        self.labelMaxComp.config(fg='#fff', font=("Roboto",11), bg=COLOR_BARRA_LATERAL, pady=10,width=5)
        self.labelMaxComp.grid(row=2, column=4, pady=5)

        self.spinnerCompresion2 = tk.Spinbox(self.frameOpHistograma, from_=0, to=255, width=5,state="disabled")
        self.spinnerCompresion2.grid(row=2, column=5, pady=5, padx=10)

        self.botonOkCompresion = tk.Button(self.frameOpHistograma, text="Ok",command=self.obtenerValSpinerCom,bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=5,state="disabled")
        self.botonOkCompresion.grid(row=2, column=6, pady=5,padx=10)

        self.labelValorDespH = tk.Label(self.frameOpHistograma, text="Val")
        self.labelValorDespH.config(fg='#fff', font=("Roboto",11), bg=COLOR_BARRA_LATERAL, pady=10,width=5)
        self.labelValorDespH.grid(row=3, column=2, pady=5)

        self.spinerDespH = tk.Spinbox(self.frameOpHistograma, from_=-255, to=255, width=5,state="disabled")
        self.spinerDespH.grid(row=3, column=3, pady=5,padx=10)

        self.botonOkDespH = tk.Button(self.frameOpHistograma, text="Ok",command=self.obtenerValSpinerDespl,bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=5,state="disabled")
        self.botonOkDespH.grid(row=3, column=4, pady=5,padx=10)

    def configurarSubMenuEditar(self):
        self.labelSubMenu = tk.Label(self.subMenuEditar, text="Editar")
        self.labelSubMenu.config(fg='#fff', font=("Roboto", 12), bg=COLOR_BARRA_LATERAL, pady=10, width=20)
        self.labelSubMenu.grid(row=0, column=0, columnspan=2)
        
        self.botonBrillo = tk.Button(self.subMenuEditar, text="Brillo", command=lambda: self.botonesMenuEditar("brillo"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonBrillo.grid(row=1, column=0, pady=5)

        self.botonContraste = tk.Button(self.subMenuEditar, text="Contraste", command=lambda: self.botonesMenuEditar("contraste"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonContraste.grid(row=4, column=0, pady=5)
        
        self.botonRotar90 = tk.Button(self.subMenuEditar, text="Rotar 90°",command=lambda: self.actualizarImgCanvas(rotar90(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonRotar90.grid(row=7, column=0, pady=5)
        
        self.botonRotarMenos90 = tk.Button(self.subMenuEditar, text="Rotar -90°",command=lambda: self.actualizarImgCanvas(rotarMenos90(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonRotarMenos90.grid(row=8, column=0, pady=5)
        
        self.botonEspejo = tk.Button(self.subMenuEditar, text="Espejo", command=lambda: self.botonesMenuEditar("espejo"), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17)  
        self.botonEspejo.grid(row=9, column=0, pady=5)

        self.botonDesplazamiento = tk.Button(self.subMenuEditar, text="Desplazamiento", command=lambda: self.botonesMenuEditar("desplazamiento"), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17) 
        self.botonDesplazamiento.grid(row=12, column=0, pady=5)
        
        
        self.botonLimpiar = tk.Button(self.subMenuEditar, text="Limpiar Región", command=lambda: self.botonesMenuEditar("limpieza"), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17) 
        self.botonLimpiar.grid(row=17, column=0, pady=5)
        
        
        self.botonCopia = tk.Button(self.subMenuEditar, text="Copiar Región", command=lambda: self.botonesMenuEditar("copia"), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17) 
        self.botonCopia.grid(row=19, column=0, pady=5)
        
        
        self.botonZoom = tk.Button(self.subMenuEditar, text="Zoom", command=lambda: self.botonesMenuEditar("zoom"), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17) 
        self.botonZoom.grid(row=21, column=0, pady=5)
        
        
        self.botonCambiarPixeles = tk.Button(self.subMenuEditar, text="Pixeles aleatorios", command=lambda: self.botonesMenuEditar("cambiarPixeles"), bd=0, bg= COLOR_BARRA_LATERAL, fg="white", width=17) 
        self.botonCambiarPixeles.grid(row=23, column=0, pady=5)
        
        self.botonRecorteIntensidad = tk.Button(self.subMenuEditar, text="Recorte de Intensidad", command=lambda: self.botonesMenuEditar("intensidad"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonRecorteIntensidad.grid(row=25, column=0, pady=5)
        
        self.botonAjusteLogaritmico = tk.Button(self.subMenuEditar, text="Ajuste Logaritmico", command=lambda: self.botonesMenuEditar("logaritmico"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonAjusteLogaritmico.grid(row=29, column=0, pady=5)
        
        self.botonAjustePotencial = tk.Button(self.subMenuEditar, text="Ajuste Potencial", command=lambda: self.botonesMenuEditar("potencial"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white", width=17)
        self.botonAjustePotencial.grid(row=32, column=0, pady=5)
        
        self.slider_brillo = None
        self.boton_ok_brillo = None

        self.slider_contraste = None
        self.boton_ok_contraste = None
        
        self.botonEspejoHorizontal = None
        self.botonEspejoVertical = None
        
        self.botonDesplazarArriba = None
        self.botonDesplazarAbajo = None
        self.botonDesplazarDerecha = None
        self.botonDesplazarIzquierda = None
        
        self.LimpiezaFlag =False
        self.CopiaFlag = False
        self.ZoomFlag = False
        self.CambiarPixelesFlag = False
        
        self.botonCancelarLimpieza = None
        self.botonCancelarCopia = None
        self.botonCancelarZoom = None
        self.botonCancelarCambiarPixeles = None

        
        self.spinner_intensidad = None
        self.spinner_intensidad2 = None
        self.boton_ok_intensidad = None
        self.spinner_logaritmico= None
        self.boton_ok_logaritmico = None
        self.spinner_potencialC= None
        self.boton_ok_potencial = None
        self.spinner_potencialY= None

    def botonesMenuEditar(self, tipo):
        if tipo == "brillo":
            if self.slider_brillo and self.boton_ok_brillo:
                self.slider_brillo.destroy()
                self.boton_ok_brillo.destroy()
                self.slider_brillo = None
                self.boton_ok_brillo = None
            else:
                self.slider_brillo = tk.Scale(self.subMenuEditar, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Entre 0 y 2", bg='#333', fg='white', troughcolor='#888', highlightbackground='#333')
                self.slider_brillo.grid(row=2, column=0, pady=5)
                self.boton_ok_brillo = tk.Button(self.subMenuEditar, text="Ok", command=self.aplicarBrillo, bd=0, bg='#333', fg="white")
                self.boton_ok_brillo.grid(row=3, column=0, pady=5)
        elif tipo == "contraste":
            if self.slider_contraste and self.boton_ok_contraste:
                self.slider_contraste.destroy()
                self.boton_ok_contraste.destroy()
                self.slider_contraste = None
                self.boton_ok_contraste = None
            else:
                self.slider_contraste = tk.Scale(self.subMenuEditar, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Entre 0 y 2", bg='#333', fg='white', troughcolor='#888', highlightbackground='#333')
                self.slider_contraste.grid(row=5, column=0, pady=5)
                self.boton_ok_contraste = tk.Button(self.subMenuEditar, text="Ok", command=self.aplicarContraste, bd=0, bg='#333', fg="white")
                self.boton_ok_contraste.grid(row=6, column=0, pady=5)
        elif tipo == "espejo":
            if self.botonEspejoHorizontal and self.botonEspejoVertical:
                self.botonEspejoHorizontal.destroy()
                self.botonEspejoVertical.destroy()
                self.botonEspejoHorizontal = None
                self.botonEspejoVertical = None
            else:
                self.botonEspejoHorizontal = tk.Button(self.subMenuEditar, text="Espejo Horizontal",command=lambda: self.actualizarImgCanvas(espejoHorizontal(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white") 
                self.botonEspejoHorizontal.grid(row=10, column=0, pady=5)
                self.botonEspejoVertical = tk.Button(self.subMenuEditar, text="Espejo Vertical",command=lambda: self.actualizarImgCanvas(espejoVertical(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white")  
                self.botonEspejoVertical.grid(row=11, column=0, pady=5)
        elif tipo == "desplazamiento":
            if self.botonDesplazarArriba and self.botonDesplazarAbajo and self.botonDesplazarDerecha and self.botonDesplazarIzquierda:
                self.botonDesplazarArriba.destroy()
                self.botonDesplazarAbajo.destroy()
                self.botonDesplazarDerecha.destroy()
                self.botonDesplazarIzquierda.destroy()
                self.botonDesplazarArriba = None
                self.botonDesplazarAbajo = None
                self.botonDesplazarDerecha = None
                self.botonDesplazarIzquierda = None
            else:
                self.botonDesplazarArriba = tk.Button(self.subMenuEditar, text="Arriba",command=lambda: self.actualizarImgCanvas(desplazamientoUp(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white")  
                self.botonDesplazarArriba.grid(row=13, column=0, pady=5)
                self.botonDesplazarAbajo = tk.Button(self.subMenuEditar, text="Abajo",command=lambda: self.actualizarImgCanvas(desplazamientoDown(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white") 
                self.botonDesplazarAbajo.grid(row=14, column=0, pady=5)
                self.botonDesplazarDerecha = tk.Button(self.subMenuEditar, text="Derecha",command=lambda: self.actualizarImgCanvas(desplazamientoRight(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white")  
                self.botonDesplazarDerecha.grid(row=15, column=0, pady=5)
                self.botonDesplazarIzquierda = tk.Button(self.subMenuEditar, text="Izquierda",command=lambda: self.actualizarImgCanvas(desplazamientoLeft(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white")  
                self.botonDesplazarIzquierda.grid(row=16, column=0, pady=5)
        elif tipo == "limpieza":
            self.LimpiezaFlag = not self.LimpiezaFlag
            if self.LimpiezaFlag:
                self.botonCancelarLimpieza = tk.Button(self.subMenuEditar, text="Cancelar", command=lambda: self.botonesMenuEditar("limpieza"), bd=0, bg='#333', fg="white")
                self.botonCancelarLimpieza.grid(row=18, column=0, pady=5)
                banderaClick(self.LimpiezaFlag)
                self.limpieza_thread = threading.Thread(target=self.aplicarLimpieza)
                self.limpieza_thread.start()
                self.botonCopia.config(state=tk.DISABLED)
                self.botonZoom.config(state=tk.DISABLED)
                self.botonCambiarPixeles.config(state=tk.DISABLED)
            else:
                if self.botonCancelarLimpieza:
                    self.botonCancelarLimpieza.destroy()
                    self.botonCancelarLimpieza = None
                if hasattr(self, 'limpieza_thread') and self.limpieza_thread.is_alive():
                    self.LimpiezaFlag = False  
                banderaClick(self.LimpiezaFlag)
                self.botonCopia.config(state=tk.NORMAL)
                self.botonZoom.config(state=tk.NORMAL)
                self.botonCambiarPixeles.config(state=tk.NORMAL)
        elif tipo == "copia":
            self.CopiaFlag = not self.CopiaFlag
            if self.CopiaFlag:
                self.botonCancelarCopia = tk.Button(self.subMenuEditar, text="Cancelar", command=lambda: self.botonesMenuEditar("copia"), bd=0, bg='#333', fg="white")
                self.botonCancelarCopia.grid(row=20, column=0, pady=5)
                banderaClick(self.CopiaFlag)
                self.copia_thread = threading.Thread(target=self.aplicarCopia)
                self.copia_thread.start()
                self.botonLimpiar.config(state=tk.DISABLED)
                self.botonZoom.config(state=tk.DISABLED)
                self.botonCambiarPixeles.config(state=tk.DISABLED)
            else:
                if self.botonCancelarCopia:
                    self.botonCancelarCopia.destroy()
                    self.botonCancelarCopia = None
                if hasattr(self, 'copia_thread') and self.copia_thread.is_alive():
                    self.CopiaFlag = False
                banderaClick(self.CopiaFlag)
                self.botonLimpiar.config(state=tk.NORMAL)
                self.botonZoom.config(state=tk.NORMAL)
                self.botonCambiarPixeles.config(state=tk.NORMAL)
                    
        elif tipo == "zoom":
            self.ZoomFlag = not self.ZoomFlag
            if self.ZoomFlag:
                self.botonCancelarZoom = tk.Button(self.subMenuEditar, text="Cancelar", command=lambda: self.botonesMenuEditar("zoom"), bd=0, bg='#333', fg="white")
                self.botonCancelarZoom.grid(row=22, column=0, pady=5)
                banderaClick(self.ZoomFlag)
                self.zoom_thread = threading.Thread(target=self.aplicarZoom)
                self.zoom_thread.start()
                self.botonLimpiar.config(state=tk.DISABLED)
                self.botonCopia.config(state=tk.DISABLED)
                self.botonCambiarPixeles.config(state=tk.DISABLED)
            else:
                if self.botonCancelarZoom:
                    self.botonCancelarZoom.destroy()
                    self.botonCancelarZoom = None
                if hasattr(self, 'zoom_thread') and self.zoom_thread.is_alive():
                    self.ZoomFlag = False
                self.ZoomFlag
                self.botonLimpiar.config(state=tk.NORMAL)
                self.botonCopia.config(state=tk.NORMAL)
                self.botonCambiarPixeles.config(state=tk.NORMAL)
                
        elif tipo == "cambiarPixeles":
            self.CambiarPixelesFlag = not self.CambiarPixelesFlag
            if self.CambiarPixelesFlag:
                self.botonCancelarCambiarPixeles = tk.Button(self.subMenuEditar, text="Cancelar", command=lambda: self.botonesMenuEditar("cambiarPixeles"), bd=0, bg='#333', fg="white")
                self.botonCancelarCambiarPixeles.grid(row=24, column=0, pady=5)
                banderaClick(self.ZoomFlag)
                self.cambiar_pixeles_thread = threading.Thread(target=self.aplicarCambiarPixeles)
                self.cambiar_pixeles_thread.start()
                self.botonLimpiar.config(state=tk.DISABLED)
                self.botonCopia.config(state=tk.DISABLED)
                self.botonZoom.config(state=tk.DISABLED)
            else:
                if self.botonCancelarCambiarPixeles:
                    self.botonCancelarCambiarPixeles.destroy()
                    self.botonCancelarCambiarPixeles = None
                if hasattr(self, 'cambiar_pixeles_thread') and self.cambiar_pixeles_thread.is_alive():
                    self.CambiarPixelesFlag = False
                banderaClick(self.ZoomFlag)
                self.botonLimpiar.config(state=tk.NORMAL)
                self.botonCopia.config(state=tk.NORMAL)
                self.botonZoom.config(state=tk.NORMAL)
                
        elif tipo == "intensidad":
            if self.spinner_intensidad and self.boton_ok_intensidad:
                self.spinner_intensidad.destroy()
                self.spinner_intensidad2.destroy()
                self.boton_ok_intensidad.destroy()
                self.spinner_intensidad = None
                self.spinner_intensidad2 = None
                self.boton_ok_intensidad = None
            else:
                self.spinner_intensidad = tk.Spinbox(self.subMenuEditar, from_=0, to=255, bg='#333', fg='white', width=5)
                self.spinner_intensidad.grid(row=26, column=0, pady=5)
                self.spinner_intensidad2 = tk.Spinbox(self.subMenuEditar, from_=0, to=255, bg='#333', fg='white', width=5)
                self.spinner_intensidad2.grid(row=27, column=0, pady=5)
                self.boton_ok_intensidad = tk.Button(self.subMenuEditar, text="Ok", command=self.aplicarIntensidad, bd=0, bg='#333', fg="white")
                self.boton_ok_intensidad.grid(row=28, column=0, pady=5)
        elif tipo == "logaritmico":
            if self.spinner_logaritmico and self.boton_ok_logaritmico:
                self.spinner_logaritmico.destroy()
                self.boton_ok_logaritmico.destroy()
                self.spinner_logaritmico = None
                self.boton_ok_logaritmico = None
            else:
                self.spinner_logaritmico = tk.Spinbox(self.subMenuEditar, from_=0, to=255, bg='#333', fg='white', width=5)
                self.spinner_logaritmico.grid(row=30, column=0, pady=5)
                self.boton_ok_logaritmico = tk.Button(self.subMenuEditar, text="Ok", command=self.aplicarLogaritmico, bd=0, bg='#333', fg="white")
                self.boton_ok_logaritmico.grid(row=31, column=0, pady=5)
        elif tipo == "potencial":
            if self.spinner_potencialC and self.spinner_potencialY and self.boton_ok_potencial:
                self.spinner_potencialC.destroy()
                self.spinner_potencialY.destroy()
                self.boton_ok_potencial.destroy()
                self.spinner_potencialC = None
                self.spinner_potencialY = None
                self.boton_ok_potencial = None
            else:
                self.spinner_potencialC = tk.Spinbox(self.subMenuEditar, from_=0, to=255, bg='#333', fg='white', width=5)
                self.spinner_potencialC.grid(row=33, column=0, pady=5)
                self.spinner_potencialY = tk.Spinbox(self.subMenuEditar, from_=0, to=5, increment=0.2, bg='#333', fg='white', width=5)
                self.spinner_potencialY.grid(row=34, column=0, pady=5)
                self.boton_ok_potencial = tk.Button(self.subMenuEditar, text="Ok", command=self.aplicarPotencial, bd=0, bg='#333', fg="white")
                self.boton_ok_potencial.grid(row=35, column=0, pady=5)

    
    def aplicarLimpieza(self):
        while self.LimpiezaFlag:
            self.actualizarImgCanvas(limpieza(self.img, self.canvasCuerpo))
            self.after(100, self.aplicarLimpieza)

    def aplicarCopia(self):
        while self.CopiaFlag:
            self.actualizarImgCanvas(copia(self.img,self.canvasCuerpo))
            self.after(100, self.aplicarCopia)

    def aplicarZoom(self):
        while self.ZoomFlag:
            self.actualizarImgCanvas(zoom(self.img,self.canvasCuerpo))
            self.after(100, self.aplicarZoom)

    def aplicarCambiarPixeles(self):
        while self.CambiarPixelesFlag:
            self.actualizarImgCanvas(cambiarPixeles(self.img,self.canvasCuerpo))
            self.after(100, self.aplicarCambiarPixeles)
        
    def aplicarBrillo(self):
        valor_brillo = self.slider_brillo.get()
        if 0 <= valor_brillo <= 2:
            self.actualizarImgCanvas(brillo(self.img, valor_brillo))
    
    def aplicarContraste(self):
        valor_contraste = self.slider_contraste.get()
        if 0 <= valor_contraste <= 2:
            self.actualizarImgCanvas(contraste(self.img, valor_contraste))
    
    def aplicarIntensidad(self):
        valor_Intensidad1 = int(self.spinner_intensidad.get())
        valor_Intensidad2 = int(self.spinner_intensidad2.get())
        if 0 <= valor_Intensidad1 <= 255 and 0 <= valor_Intensidad1 <= 255 and valor_Intensidad1 < valor_Intensidad2:
            self.actualizarImgCanvas(intensityLevelSlicing(self.img, valor_Intensidad1,valor_Intensidad2))
            
    def aplicarLogaritmico(self):
        valor_Logaritmico = int(self.spinner_logaritmico.get())
        if 0 <= valor_Logaritmico <= 255:
            self.actualizarImgCanvas(transformacionLog(self.img, valor_Logaritmico))

    def aplicarPotencial(self):
        c = int(self.spinner_potencialC.get())
        y = float(self.spinner_potencialY.get())
        if 0 <= c <= 255 and 0 <= y <= 5:
            self.actualizarImgCanvas(transformacionPot(self.img, c, y))

    def configurarSubMenuColor(self):
        self.labelColor = tk.Label(self.subMenuColor, text="Color")
        self.labelColor.config(fg='#fff', font=("Roboto",12), bg=COLOR_BARRA_LATERAL, pady=10,width=20)
        self.labelColor.pack(side=tk.TOP,expand=False)

        self.botonBN = tk.Button(self.subMenuColor, text="Blanco y negro",command=lambda: self.actualizarImgCanvas(escalaGrises(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonBN.pack(side=tk.TOP,pady=(0, 10))

        self.botonInversion = tk.Button(self.subMenuColor, text="Negativo",command=lambda: self.actualizarImgCanvas(inversion(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonInversion.pack(side=tk.TOP, pady=(0, 10))

        self.botonSepia = tk.Button(self.subMenuColor, text="Sepia Calido",command=lambda: self.actualizarImgCanvas(sepiaCalido(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonSepia.pack(side=tk.TOP, pady=(0, 10))

        self.botonSepiaFrio = tk.Button(self.subMenuColor, text="Sepia Frio",command=lambda: self.actualizarImgCanvas(sepiaFrio(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonSepiaFrio.pack(side=tk.TOP, pady=(0, 10))

        self.botonSepiaVintage = tk.Button(self.subMenuColor, text="Sepia Vintage",command=lambda: self.actualizarImgCanvas(sepiaVintage(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonSepiaVintage.pack(side=tk.TOP, pady=(0, 10))

        self.botonSepiaIntenso = tk.Button(self.subMenuColor, text="Sepia Intenso",command=lambda: self.actualizarImgCanvas(sepiaIntenso(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonSepiaIntenso.pack(side=tk.TOP, pady=(0, 10))

        self.botonSepiaSuave = tk.Button(self.subMenuColor, text="Sepia Suave",command=lambda: self.actualizarImgCanvas(sepiaSuave(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=10)
        self.botonSepiaSuave.pack(side=tk.TOP, pady=(0, 10))

    def configurarSubMenuFitros(self):
        self.labelFiltros = tk.Label(self.subMenuFiltros, text="Filtros")
        self.labelFiltros.config(fg='#fff', font=("Roboto",12), bg=COLOR_BARRA_LATERAL, pady=10,width=20)
        self.labelFiltros.pack(side=tk.TOP,expand=False)

        self.botonDesenfoque = tk.Button(self.subMenuFiltros, text="Desenfoque",command=lambda: self.actualizarImgCanvas(desenfoque(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonDesenfoque.pack(side=tk.TOP, pady=(0, 10))

        self.botonDetalle = tk.Button(self.subMenuFiltros, text="Detalle",command=lambda: self.actualizarImgCanvas(detalle(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonDetalle.pack(side=tk.TOP, pady=(0, 10))

        self.botonSuavizado = tk.Button(self.subMenuFiltros, text="Suavizado",command=lambda: self.actualizarImgCanvas(suavizado(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonSuavizado.pack(side=tk.TOP, pady=(0, 10))

        self.botonNitidez = tk.Button(self.subMenuFiltros, text="Nitidez",command=lambda: self.actualizarImgCanvas(nitidez(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonNitidez.pack(side=tk.TOP, pady=(0, 10))

        self.botonRelieve = tk.Button(self.subMenuFiltros, text="Relieve",command=lambda: self.actualizarImgCanvas(relieve(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonRelieve.pack(side=tk.TOP, pady=(0, 10))

        self.botonResBordes = tk.Button(self.subMenuFiltros, text="Resaltar Bordes",command=lambda: self.actualizarImgCanvas(resaltarBordes(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonResBordes.pack(side=tk.TOP, pady=(0, 10))

        self.botonRealBordes = tk.Button(self.subMenuFiltros, text="Realzar Bordes",command=lambda: self.actualizarImgCanvas(realzarBordes(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonRealBordes.pack(side=tk.TOP, pady=(0, 10))

        self.botonBordes = tk.Button(self.subMenuFiltros, text="Bordes",command=lambda: self.actualizarImgCanvas(detectarBordes(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=12)
        self.botonBordes.pack(side=tk.TOP, pady=(0, 10))
    

    def configurarSubMenuRetoque(self):
        self.labelRetoque = tk.Label(self.subMenuRetoque, text="Retoque")
        self.labelRetoque.config(fg='#fff', font=("Roboto", 12), bg=COLOR_BARRA_LATERAL, pady=10, width=20)
        self.labelRetoque.grid(row=0, column=0, columnspan=2)

        self.botonImperfecciones = tk.Button(self.subMenuRetoque, text="Eliminar Imperfecciones", command=lambda: self.botonesMenuRetoque("eliminarImperfecciones"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white")
        self.botonImperfecciones.grid(row=1, column=0, pady=5)

        self.botonBorrarObjetos = tk.Button(self.subMenuRetoque, text="Eliminar Objetos", command=lambda: self.botonesMenuRetoque("removerObjetos"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white")
        self.botonBorrarObjetos.grid(row=3, column=0, pady=5)

        self.botonBorrarRostro = tk.Button(self.subMenuRetoque, text="Eliminar Rostro", command=lambda: self.botonesMenuRetoque("removerRostro"), bd=0, bg=COLOR_BARRA_LATERAL, fg="white")
        self.botonBorrarRostro.grid(row=7, column=0, pady=5)
        
        self.ImperfeccionesFlag = False
        self.botonCancelarImperfecciones = None

        self.removerObjetosFlag = False
        self.botonCancelarObjetos = None

        self.removerRostroFlag = False
        self.botonCancelarRostro = None

        self.spinner_size = None
        self.label_info = None
        
        self.spinnerRadio = None

    def botonesMenuRetoque(self, tipo):
        if tipo == "eliminarImperfecciones":
            self.ImperfeccionesFlag = not self.ImperfeccionesFlag
            if self.ImperfeccionesFlag:
                self.botonCancelarImperfecciones = tk.Button(self.subMenuRetoque, text="Cancelar", command=lambda: self.botonesMenuRetoque("eliminarImperfecciones"), bd=0, bg='#333', fg="white")
                self.botonCancelarImperfecciones.grid(row=2, column=0, pady=5)
                banderaClick(self.ImperfeccionesFlag)
                self.imperfecciones_thread = threading.Thread(target=self.aplicarImperfecciones)
                self.imperfecciones_thread.start()
                self.botonBorrarObjetos.config(state=tk.DISABLED)
                self.botonBorrarRostro.config(state=tk.DISABLED)
            else:
                if self.botonCancelarImperfecciones:
                    self.botonCancelarImperfecciones.destroy()
                    self.botonCancelarImperfecciones = None
                if hasattr(self, 'imperfecciones_thread') and self.imperfecciones_thread.is_alive():
                    self.ImperfeccionesFlag = False
                banderaClick(self.ImperfeccionesFlag)
                self.botonBorrarObjetos.config(state=tk.NORMAL)
                self.botonBorrarRostro.config(state=tk.NORMAL)

        elif tipo == "removerObjetos":
            self.removerObjetosFlag = not self.removerObjetosFlag
            if self.removerObjetosFlag:
                self.label_info = tk.Label(self.subMenuRetoque, text="", bg='#333', fg="white")
                self.label_info.grid(row=5, column=0, pady=5)
                self.botonCancelarObjetos = tk.Button(self.subMenuRetoque, text="Cancelar", command=lambda: self.botonesMenuRetoque("removerObjetos"), bd=0, bg='#333', fg="white")
                self.botonCancelarObjetos.grid(row=6, column=0, pady=5)
                self.spinner_size = tk.Scale(self.subMenuRetoque, from_=10, to=50, resolution=1, orient=tk.HORIZONTAL, label="Tamaño", bg='#333', fg='white', troughcolor='#888', highlightbackground='#333')
                self.spinner_size.grid(row=4, column=0, pady=5)
                banderaObjeto(self.removerObjetosFlag)
                self.removerObjetos_thread = threading.Thread(target=self.aplicarRemoverObjetos, args=(self.label_info,))
                self.removerObjetos_thread.start()
                self.botonImperfecciones.config(state=tk.DISABLED)
                self.botonBorrarRostro.config(state=tk.DISABLED)
            else:
                if self.botonCancelarObjetos and self.spinner_size:
                    self.spinner_size.destroy()
                    self.spinner_size = None
                    self.botonCancelarObjetos.destroy()
                    self.botonCancelarObjetos = None
                    self.label_info.destroy()
                    self.label_info = None
                if hasattr(self, 'removerObjetos_thread') and self.removerObjetos_thread.is_alive():
                    self.removerObjetosFlag = False
                banderaObjeto(self.removerObjetosFlag)
                self.botonImperfecciones.config(state=tk.NORMAL)
                self.botonBorrarRostro.config(state=tk.NORMAL)    
        elif tipo == "removerRostro":
            self.removerRostroFlag = not self.removerRostroFlag
            if self.removerRostroFlag:
                self.botonCancelarRostro = tk.Button(self.subMenuRetoque, text="Cancelar", command=lambda: self.botonesMenuRetoque("removerRostro"), bd=0, bg='#333', fg="white")
                self.botonCancelarRostro.grid(row=9, column=0, pady=5)
                self.spinnerRadio = tk.Scale(self.subMenuRetoque, from_=50, to=150, resolution=10, orient=tk.HORIZONTAL, label="Precisión", bg='#333', fg='white', troughcolor='#888', highlightbackground='#333')
                self.spinnerRadio.grid(row=8, column=0, pady=5)
                banderaClick(self.removerRostroFlag)
                self.removerRostro_thread = threading.Thread(target=self.aplicarRemoverRostro)
                self.removerRostro_thread.start()
                self.botonImperfecciones.config(state=tk.DISABLED)
                self.botonBorrarObjetos.config(state=tk.DISABLED)
            else:
                if self.botonCancelarRostro:
                    self.botonCancelarRostro.destroy()
                    self.spinnerRadio.destroy()
                    self.botonCancelarRostro = None
                    self.spinnerRadio = None
                if hasattr(self, 'removerRostro_thread') and self.removerRostro_thread.is_alive():
                    self.removerRostroFlag = False
                banderaClick(self.removerRostroFlag)
                self.botonImperfecciones.config(state=tk.NORMAL)
                self.botonBorrarObjetos.config(state=tk.NORMAL)
    
    def aplicarImperfecciones(self):
        while self.ImperfeccionesFlag:
            self.actualizarImgCanvas(removerImperfecciones(self.img, self.canvasCuerpo))
            self.after(100, self.aplicarImperfecciones)

    def aplicarRemoverObjetos(self, label_info):
        while self.removerObjetosFlag:
            size = int(self.spinner_size.get())
            if 0 <= size <= 30:
                self.img = removerObjetos(self.img, self.canvasCuerpo, size, label_info)
                self.actualizarImgCanvas(self.img)
            self.after(100, self.aplicarRemoverObjetos, label_info)

    def aplicarRemoverRostro(self):
        while self.removerRostroFlag:
            radio = int(self.spinnerRadio.get())
            if 50 <= radio <= 150:
                self.actualizarImgCanvas(eliminarRostros(self.img, self.canvasCuerpo, radio, self))
            self.after(100, self.aplicarRemoverRostro)
        
    def configurarSubMenuMorfologia(self):
        self.labelMorfologia = tk.Label(self.subMenuMorfologia, text="Morfologia")
        self.labelMorfologia.config(fg='#fff', font=("Roboto",12), bg=COLOR_BARRA_LATERAL, pady=10,width=20)
        self.labelMorfologia.pack(side=tk.TOP,expand=False)
        
        self.botonErosion = tk.Button(self.subMenuMorfologia, text="Erosión",command=lambda: self.actualizarImgCanvas(erosion(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonErosion.pack(side=tk.TOP,pady=(0, 20))
        
        self.botonDilatacion = tk.Button(self.subMenuMorfologia, text="Dilatación",command=lambda: self.actualizarImgCanvas(dilatacion(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonDilatacion.pack(side=tk.TOP,pady=(0, 20))
        
        self.botonApertura = tk.Button(self.subMenuMorfologia, text="Disminuir protuberancias",command=lambda: self.actualizarImgCanvas(apertura(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonApertura.pack(side=tk.TOP,pady=(0, 20))
        
        self.botonClausura = tk.Button(self.subMenuMorfologia, text="Rellena concavidades",command=lambda: self.actualizarImgCanvas(clausura(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonClausura.pack(side=tk.TOP,pady=(0, 20))
        
        self.botonEliminarRuido = tk.Button(self.subMenuMorfologia, text="Eliminar Ruido",command=lambda: self.actualizarImgCanvas(eliminarRuido(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonEliminarRuido.pack(side=tk.TOP,pady=(0, 20))
        
        self.botonResaltarBordes = tk.Button(self.subMenuMorfologia, text="Resaltar Bordes",command=lambda: self.actualizarImgCanvas(resaltarBordes(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonResaltarBordes.pack(side=tk.TOP,pady=(0, 20))
        
        self.botonPolaridad = tk.Button(self.subMenuMorfologia, text="Polarizar",command=lambda: self.actualizarImgCanvas(polarizar(self.img)), bd=0, bg= COLOR_BARRA_LATERAL, fg="white",width=20)
        self.botonPolaridad.pack(side=tk.TOP,pady=(0, 20))

    def habilitarBoton(self):
        self.botonClean.config(state="normal")
        self.botonEditar.config(state="normal")
        self.botonColor.config(state="normal")
        self.botonFiltros.config(state="normal")
        self.botonRetoque.config(state="normal")
        self.botonMas.config(state="normal")
        self.botonGuardar.config(state="normal")
        self.botonUnDo.config(state="normal")
        self.botonReDo.config(state="normal")
        self.botonEcualizar.config(state="normal")
        self.botonExpL.config(state="normal")
        self.botonThreshold.config(state="normal")
        self.spinnerCompresion1.config(state="normal")
        self.spinnerCompresion2.config(state="normal")
        self.spinerDespH.config(state="normal")
        self.botonOkCompresion.config(state="normal")
        self.botonOkDespH.config(state="normal")
        self.botonHuff.config(state="normal")
        
        

    def toggle_Menu(self):
        if self.menuLateral.winfo_ismapped():
            self.menuLateral.pack_forget()
        else:
            if self.frameHistograma.winfo_ismapped():
                self.frameHistograma.pack_forget()
            if self.subMenuEditar.winfo_ismapped():
                self.subMenuEditar.pack_forget()
            if self.subMenuFiltros.winfo_ismapped():
                self.subMenuFiltros.pack_forget()
            if self.subMenuColor.winfo_ismapped():
                self.subMenuColor.pack_forget()
            if self.subMenuRetoque.winfo_ismapped():
                self.subMenuRetoque.pack_forget()
            if self.subMenuMorfologia.winfo_ismapped():
                self.subMenuMorfologia.pack_forget()
            self.menuLateral.pack(side=tk.LEFT, fill='y')

    def toggleSubMenuEditar(self):
        if self.subMenuEditar.winfo_ismapped():
            self.subMenuEditar.pack_forget()
        else:
            if self.frameHistograma.winfo_ismapped():
                self.frameHistograma.pack_forget()
            if self.subMenuFiltros.winfo_ismapped():
                self.subMenuFiltros.pack_forget()
            if self.subMenuColor.winfo_ismapped():
                self.subMenuColor.pack_forget()
            if self.subMenuRetoque.winfo_ismapped():
                self.subMenuRetoque.pack_forget()
            if self.subMenuMorfologia.winfo_ismapped():
                self.subMenuMorfologia.pack_forget()
            self.subMenuEditar.pack(side=tk.LEFT, fill='y')

    def toggleSubMenuColor(self):
        if self.subMenuColor.winfo_ismapped():
            self.subMenuColor.pack_forget()
        else:
            if self.frameHistograma.winfo_ismapped():
                self.frameHistograma.pack_forget()
            if self.subMenuEditar.winfo_ismapped():
                self.subMenuEditar.pack_forget()
            if self.subMenuFiltros.winfo_ismapped():
                self.subMenuFiltros.pack_forget()
            if self.subMenuRetoque.winfo_ismapped():
                self.subMenuRetoque.pack_forget()
            if self.subMenuMorfologia.winfo_ismapped():
                self.subMenuMorfologia.pack_forget()
            self.subMenuColor.pack(side=tk.LEFT, fill='y')

    def toggleSubMenuFiltros(self):
        if self.subMenuFiltros.winfo_ismapped():
            self.subMenuFiltros.pack_forget()
        else:
            if self.frameHistograma.winfo_ismapped():
                self.frameHistograma.pack_forget()
            if self.subMenuEditar.winfo_ismapped():
                self.subMenuEditar.pack_forget()
            if self.subMenuColor.winfo_ismapped():
                self.subMenuColor.pack_forget()
            if self.subMenuRetoque.winfo_ismapped():
                self.subMenuRetoque.pack_forget()
            if self.subMenuMorfologia.winfo_ismapped():
                self.subMenuMorfologia.pack_forget()
            self.subMenuFiltros.pack(side=tk.LEFT, fill='y')

    def toggleSubMenuRetoque(self):
        if self.subMenuRetoque.winfo_ismapped():
            self.subMenuRetoque.pack_forget()
        else:
            if self.frameHistograma.winfo_ismapped():
                self.frameHistograma.pack_forget()
            if self.subMenuEditar.winfo_ismapped():
                self.subMenuEditar.pack_forget()
            if self.subMenuFiltros.winfo_ismapped():
                self.subMenuFiltros.pack_forget()
            if self.subMenuColor.winfo_ismapped():
                self.subMenuColor.pack_forget()
            if self.subMenuMorfologia.winfo_ismapped():
                self.subMenuMorfologia.pack_forget()
            self.subMenuRetoque.pack(side=tk.LEFT, fill='y')

    def toggleSubMenuMorfologia(self):
        if self.subMenuMorfologia.winfo_ismapped():
            self.subMenuMorfologia.pack_forget()
        else:
            if self.frameHistograma.winfo_ismapped():
                self.frameHistograma.pack_forget()
            if self.subMenuEditar.winfo_ismapped():
                self.subMenuEditar.pack_forget()
            if self.subMenuFiltros.winfo_ismapped():
                self.subMenuFiltros.pack_forget()
            if self.subMenuColor.winfo_ismapped():
                self.subMenuColor.pack_forget()
            if self.subMenuRetoque.winfo_ismapped():
                self.subMenuRetoque.pack_forget()
            self.subMenuMorfologia.pack(side=tk.LEFT, fill='y')

    def toggleHistograma(self):
        if self.frameHistograma.winfo_ismapped():
            self.frameHistograma.pack_forget()
        else:
            if self.subMenuEditar.winfo_ismapped():
                self.subMenuEditar.pack_forget()
            if self.subMenuFiltros.winfo_ismapped():
                self.subMenuFiltros.pack_forget()
            if self.subMenuColor.winfo_ismapped():
                self.subMenuColor.pack_forget()
            if self.subMenuRetoque.winfo_ismapped():
                self.subMenuRetoque.pack_forget()
            if self.subMenuMorfologia.winfo_ismapped():
                self.subMenuMorfologia.pack_forget()
            self.cuerpoPrincipal.pack_forget()
            self.frameHistograma.pack(side=tk.RIGHT, fill='both')
            self.cuerpoPrincipal.pack(side=tk.RIGHT, fill='both', expand=True)
    #carga la imagen por primera vez en el canvas
    def colocarImgCanvas(self):
        if self.primeraCarga:
            self.colocarOtraImg()
            return
        
        self.img = uImg.cargarImagen()
        self.imgWidth, self.imgHeight = self.img.size
        
        if (self.imgWidth > 1300 or self.imgHeight > 900):
            redim = uImg.redimensionarImg(self.img,int(self.imgWidth*0.70), int(self.imgHeight*0.60))
            photo = uImg.ImageTk.PhotoImage(redim)

            self.canvasCuerpo.config(width=int(self.imgWidth*0.70),height= int(self.imgHeight*0.60))
            self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo

        else:
            self.canvasCuerpo.config(width=self.imgWidth, height=self.imgHeight)
            photo = uImg.ImageTk.PhotoImage(self.img)
            self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo

        self.insertarImagen()
        self.habilitarBoton()
        self.updateBarraInf()
        self.mostrarHistograma()

        self.primeraCarga = True
    #carga otra imagen
    def colocarOtraImg(self):
        self.img = uImg.cargarImagen()
        self.imgWidth, self.imgHeight = self.img.size

        if (self.imgWidth > 1300 or self.imgHeight > 900):
            redim = uImg.redimensionarImg(self.img,int(self.imgWidth*0.70), int(self.imgHeight*0.60))
            photo = uImg.ImageTk.PhotoImage(redim)

            self.canvasCuerpo.config(width=int(self.imgWidth*0.70),height= int(self.imgHeight*0.60))
            self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo

        else:
            self.canvasCuerpo.config(width=self.imgWidth, height=self.imgHeight)
            photo = uImg.ImageTk.PhotoImage(self.img)
            self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo
        self.insertarImagen()
        self.updateBarraInf()
        self.mostrarHistograma()
        self.update
    #actualiza la img del canvas cuando se hace una operacion
    def actualizarImgCanvas(self,img):
        self.img = img
        self.imgWidth, self.imgHeight = self.img.size

        if (self.imgWidth > 1300 or self.imgHeight > 900):
            redim = uImg.redimensionarImg(self.img,int(self.imgWidth*0.70), int(self.imgHeight*0.60))
            photo = uImg.ImageTk.PhotoImage(redim)

            self.canvasCuerpo.config(width=int(self.imgWidth*0.70),height= int(self.imgHeight*0.60))
            self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo

        else:
            self.canvasCuerpo.config(width=self.imgWidth, height=self.imgHeight)
            photo = uImg.ImageTk.PhotoImage(self.img)
            self.canvasCuerpo.create_image(0,0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo

        self.insertarImagen()
        self.mostrarHistograma()
        #self.updateBarraInf()
        
    def updateBarraInf(self):
        self.labelDimensiones.config(text=f"Dim {self.imgWidth}x{self.imgHeight}")
        self.labelProfundidad.config(text=f"Prof. bits {uImg.getProfundidadColor(self.img)}")
        self.labelTamanio.config(text=f"Tamaño {uImg.getPesoImg(self.img):.2f} MB")

    def mostrarHistograma(self):
        h = uImg.calcularHistorgrama(self.img)
        h.set_size_inches(5.55,4.0)
        self.canvasHistograma.figure = h
        self.canvasHistograma.draw()

    #esta funcion hace funcionar al redo, undo y limpiar
    def updateImage(self,img):

        self.img = img
        self.imgWidth, self.imgHeight = self.img.size

        if self.imgWidth > 1300 or self.imgHeight > 900:
            redim = uImg.redimensionarImg(self.img, int(self.imgWidth * 0.70), int(self.imgHeight * 0.60))
            photo = uImg.ImageTk.PhotoImage(redim)

            self.canvasCuerpo.config(width=int(self.imgWidth * 0.70), height=int(self.imgHeight * 0.60))
            self.canvasCuerpo.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo
        else:
            self.canvasCuerpo.config(width=self.imgWidth, height=self.imgHeight)
            photo = uImg.ImageTk.PhotoImage(self.img)
            self.canvasCuerpo.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvasCuerpo.image_ref = photo

        self.mostrarHistograma()
        #self.updateBarraInf()


    def insertarImagen(self):
        self.listaImagenes.append(self.img)
        self.contadorImagenes += 1
        
    def unDo(self):
        if self.contadorImagenes > 0:
            self.contadorImagenes -= 1
            self.img = self.listaImagenes[self.contadorImagenes]
            self.updateImage(self.img)
            
    def reDo(self):
        if self.contadorImagenes < len(self.listaImagenes)-1 and self.contadorImagenes >= 0:
            self.contadorImagenes += 1
            self.img = self.listaImagenes[self.contadorImagenes]
            self.updateImage(self.img)

    def limpiar(self):
        self.updateImage(self.listaImagenes[0])
        self.listaImagenes = []
        self.contadorImagenes = 0

    def generarHdr(self):
        ventanaHDR = VentanaHDR()
        ventanaHDR.wait_window()
        imgHdr = returnImgHdr()
        if imgHdr != None:
            self.updateImage(imgHdr)
            self.habilitarBoton()
            self.insertarImagen()

    def obtenerValSpinerCom(self):
        sm = int(self.spinnerCompresion1.get())
        sM = int(self.spinnerCompresion2.get())

        if sm != sM and sm < sM:
            self.actualizarImgCanvas(compresion(self.img,sm,sM))

    def obtenerValSpinerDespl(self):
        val = int(self.spinerDespH.get())
        self.actualizarImgCanvas(desplazamiento(self.img,val))
        pass
            


    



        


    
