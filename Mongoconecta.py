
import pymongo
import tkinter as tk
from tkinter import messagebox

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Ciudadanos']
mycol = mydb['Registrados']

lst = [('Nombre','Apellido','Edad','Cédula','Género','Discapa','Dirección','Bono','Emprende')]

def callback(event):
    li=[]
    li=event.widget._values
    cnombre1.set(lst[li[1]][2])
    capelli1.set(lst[li[1]][3])
    cedad.set(lst[li[1]][4])
    cidentidad.set(lst[li[2]][5])
    cgenero.set(lst[li[1]][6])
    cdiscapacidad.set(lst[li[2]][7])
    cdireccion.set(lst[li[1]][8])
    cbono.set(lst[li[1]][9])
    cemprende.set(lst[li[1]][10])


def creategrid(num):
    lst.clear()
    lst.append(['Nombre','Apellido','Edad','Cédula','Género','Discapa','Dirección','Bono','Emprende'])
    cursor = mycol.find({})
    for text_fromDB in cursor:
        nombre1 = str(text_fromDB['Primer nombre']).encode('utf_8').decode("utf_8")
        apellido1 = str(text_fromDB['Primer apellido']).encode('utf_8').decode("utf_8")
        edad = int(text_fromDB['Edad'])
        cedula = str(text_fromDB['Cédula']).encode('utf_8').decode("utf_8")
        genero =  str(text_fromDB['Género']).encode('utf_8').decode("utf_8")
        discapas = str(text_fromDB['Discapacidad']).encode('utf_8').decode("utf_8")
        Direccion = str(text_fromDB['Dirección']).encode('utf_8').decode("utf_8")
        bono = float(text_fromDB['Bono'])
        emprene = str(text_fromDB['Emprende']).encode('utf_8').decode("utf_8")
        lst.append([nombre1,apellido1,edad,cedula,genero,discapas,Direccion,bono,emprene])
    
    for interacion in range(len(lst)):
        for itera in range(len(lst[0])):
            mgrid = tk.Entry(window,width=10)
            mgrid.insert(tk.END,lst[interacion][itera])
            mgrid._values = mgrid.get(),interacion
            mgrid.grid(row=(interacion+1), column=(itera+3))
            mgrid.bind("<Button-1>", callback)

    if (num==1):
        for label in window.grid_slaves():
            if (int(label.grid_info()("row")) > 11):
                label.grid_forget()

def msgbox(msg,titulobar):
    result=messagebox.askokcancel(title=titulobar,message=msg)
    return result

def guarda ():
    rap=msgbox("Registro guardado","Registro")
    if (rap==True):
        mydict= {'Primer nombre':cnombre1.get(),'Primer apellido':capelli1.get(),
                 'Edad':int(cedad.get()),'Cédula':cidentidad.get(),'Género':cgenero.get(),
                 'Discapacidad':cdiscapacidad.get(),'Dirección':cdireccion.get(),'Bono':float(cbono.get()),
                 'Emprende':cemprende.get()
                }
        agregaUno = mycol.insert_one(mydict)
        creategrid(1)
        creategrid(0)


def elimina ():
    rap=msgbox("Registro eliminado","Eliminar")
    if (rap==True):
        myquerry = {'Cédula':cidentidad.get()}
        mycol.delete_one(myquerry)
    creategrid(1)
    creategrid(0)

def modifica ():
    rap=msgbox("Registro modificado","Modificar")
    if rap == True:
        myquerry = {'Cédula':cidentidad.get()}
        newvalues = {"$set":{"Primer nombre":cnombre1.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"Primer apellido":capelli1.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"edad":cedad.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"Cédula":cidentidad.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"Género":cgenero.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"Discapacidad":cdiscapacidad.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"Dirección":cdireccion.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"bono":cbono.get()}}
        mycol.update_one(myquerry,newvalues)

        newvalues = {"$set":{"Emprende":cemprende.get()}}
        mycol.update_one(myquerry,newvalues)
        creategrid(1)
        creategrid(0)

window = tk.Tk()
window.title("Base de datos del sistema")
window.geometry("1000x600")
window.config(bg="white")

label = tk.Label(window, text="Base de datos del sistema", width=30, height=1,bg= "white", anchor="center")
label.config(font=("Courter",10))
label.grid(column=2,row=1)

label = tk.Label(window, text="Primer nombre", width=15, height=1,bg= "white")
label.grid(column=1,row=2)
cnombre1 = tk.StringVar()
cnombre1 = tk.Entry(window, textvariable=cnombre1)
cnombre1.grid(column=2,row=2)


label = tk.Label(window, text="Primer apellido", width=15, height=1,bg= "white")
label.grid(column=1,row=3)
capelli1 = tk.StringVar()
capelli1 = tk.Entry(window, textvariable=capelli1)
capelli1.grid(column=2,row=3)


label = tk.Label(window, text="Edad", width=15, height=1,bg= "white")
label.grid(column=1,row=4)
cedad = tk.StringVar()
cedad = tk.Entry(window, textvariable=cedad)
cedad.grid(column=2,row=4)

label = tk.Label(window, text="Cédula", width=15, height=1,bg= "white")
label.grid(column=1,row=5)
cidentidad = tk.StringVar()
cidentidad = tk.Entry(window, textvariable=cidentidad)
cidentidad.grid(column=2,row=5)

label = tk.Label(window, text="Género", width=15, height=1,bg= "white")
label.grid(column=1,row=6)
cgenero = tk.StringVar()
cgenero = tk.Entry(window, textvariable=cgenero)
cgenero.grid(column=2,row=6)

label = tk.Label(window, text="Discapacidad", width=15, height=1,bg= "white")
label.grid(column=1,row=7)
cdiscapacidad = tk.StringVar()
cdiscapacidad = tk.Entry(window, textvariable=cdiscapacidad)
cdiscapacidad.grid(column=2,row=7)

label = tk.Label(window, text="Dirección", width=15, height=1,bg= "white")
label.grid(column=1,row=8)
cdireccion = tk.StringVar(window)
cdireccion.set("Elegir opcion")
calles=[
    'Barrio bryan','Barrio las palmas','29 de mayo','km 23 via Quevdo','Luz de américa',
    'Santo domingo','Eloy Alfaro','Barrio Cricita','Valla vista','Lotizaciones Wilson Eraso',]
menu=tk.OptionMenu(window,cdireccion,*calles)
menu.config(width=15, height=1,bg= "white")
menu.grid(column=2,row=8)


label = tk.Label(window, text="Bono", width=15, height=1,bg= "white")
label.grid(column=1,row=9)
cbono = tk.StringVar()
cbono = tk.Entry(window, textvariable=cbono)
cbono.grid(column=2,row=9)


label = tk.Label(window, text="Emprende", width=15, height=1,bg= "white")
label.grid(column=1,row=10)
cemprende = tk.StringVar()
cemprende = tk.Entry(window, textvariable=cemprende)
cemprende.grid(column=2,row=10)

creategrid(0)

savebtn = tk.Button(text="Guardar", command=guarda)
savebtn.grid(column=0,row=11)
savebtn = tk.Button(text="Eliminar", command=elimina)
savebtn.grid(column=1,row=11)
savebtn = tk.Button(text="actualizar", command=modifica)
savebtn.grid(column=2,row=11)


def main():
    window.mainloop()

if __name__ == "__main__":
    main()