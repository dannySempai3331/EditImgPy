from Vista.disenno import Principal
"""Hecho por:
Kenneth Kael Mendoza Pliego
José Daniel Pérez Mejía"""
app = Principal()

app.protocol("WM_DELETE_WINDOW", app.quit)

app.mainloop()
