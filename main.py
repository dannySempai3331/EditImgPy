from Vista.disenno import Principal

app = Principal()

app.protocol("WM_DELETE_WINDOW", app.quit)

app.mainloop()