def centrarVentana(ventana, appAncho, appLargo):
    pantallaAncho = ventana.winfo_screenwidth()
    pantallaLargo = ventana.winfo_screenheight()
    x = int((pantallaAncho / 2) - (appAncho / 2))
    y = int((pantallaLargo / 2) - (appLargo / 2))
    ventana.geometry(f'{appAncho}x{appLargo}+{x}+{y}')