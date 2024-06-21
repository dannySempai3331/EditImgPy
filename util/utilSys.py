import platform, os, datetime

"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""

def getOS():
    return platform.system()

def getUsuario():
    return os.getenv('HOME')

def getFechaHora():
    now = datetime.datetime.now()
    fechaHoraF = now.strftime("%Y%m%d%H%M%S")
    return fechaHoraF
