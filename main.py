'''Estas son las librería correspondientes para la conexión con mongoDb'''
import pymongo
import tkinter as tk
from tkinter import Scrollbar, messagebox, Frame

# Conexión con la base de datos mongoDb
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Ciudadanos']
mycol = mydb['Registrados']

'''Lista de parametros que se mostraran en la pantalla''' 
lst = [('Nº','Nombre','Apellido','Edad','Cédula','Género','Discap.','Direc.','Bono','Emprede')]

class BaseData:
    def callback(self,event):
        '''
            Sirve para dar las posiciones en la diferente columna del programa.

            PARAMETROS
            -----------
                event: any
                    
        '''
        li=[]
        li=event.widget._values
        self.cid.set(lst[li[1]][0])
        self.cnombre1.set(lst[li[1]][1])
        self.capelli1.set(lst[li[1]][2])
        self.cedad.set(lst[li[1]][3])
        self.cidentidad.set(lst[li[1]][4])
        self.cgenero.set(lst[li[1]][5])
        self.cdiscapacidad.set(lst[li[1]][6])
        self.cdireccion.set(lst[li[1]][7])
        self.cbono.set(lst[li[1]][8])
        self.cemprende.set(lst[li[1]][9])


    def creategrid(self,num):
        '''
            Método que ayudará a insertar, eliminar y modificar los datos.
            Además cumple la función de permitir ingresar caracteres especiales.

            PARAMETROS
            ----------
                num: int
                    Es el número que será evaluado después
            
            RETORNA
            --------
                Devulve un par de condicionales for...
        '''
        lst.clear()
        lst.append(['Nº','Nombre','Apellido','Edad','Cédula','Género','Discap.','Direc.','Bono','Emprede'])
        cursor = mycol.find({})
        for text_fromDB in cursor:
            personid = int(text_fromDB['id'])
            nombre1 = str(text_fromDB['Primer nombre']).encode('utf_8').decode("utf_8")
            apellido1 = str(text_fromDB['Primer apellido']).encode('utf_8').decode("utf_8")
            edad = int(text_fromDB['Edad'])
            cedula = str(text_fromDB['Cédula']).encode('utf_8').decode("utf_8")
            genero =  str(text_fromDB['Género']).encode('utf_8').decode("utf_8")
            discapas = str(text_fromDB['Discapacidad']).encode('utf_8').decode("utf_8")
            Direccion = str(text_fromDB['Dirección']).encode('utf_8').decode("utf_8")
            bono = float(text_fromDB['Bono'])
            emprene = str(text_fromDB['Emprende']).encode('utf_8').decode("utf_8")
            lst.append([personid,nombre1,apellido1,edad,cedula,genero,discapas,Direccion,bono,emprene])
        
        for interacion in range(len(lst)):
            for itera in range(len(lst[0])):
                mgrid = tk.Entry(self.window,width=11,font=('Arial',10,'bold'), bg='#8da9c9')
                mgrid.insert(tk.END,lst[interacion][itera])
                mgrid._values = mgrid.get(),interacion
                mgrid.grid(row=(interacion+15), column=(itera+4),padx=0,pady=4)
                mgrid.bind("<Button-1>", self.callback)

        if (num==1):
            for label in self.window.grid_slaves():
                if (int(label.grid_info()["row"]) > 12):
                    label.grid_forget()


    def msgbox(self,msg,titulobar):
        '''
            Permite enviar mensaje de información.

            PARAMETROS
            -----------
                msg: str
                    Es el mensaje que se imprimerá por pantalla
                titulobar: str
                    Es el título que contendrá la ventana

            Retorna
            ---------
                result
        '''
        result=messagebox.askokcancel(title=titulobar,message=msg)
        return result

    def guarda (self):
        '''
        Método que permite guardar un reegistro nuevo a la base de datos
        Atraves de los campos que se vallan a ingresar.
        '''
        rap=self.msgbox("Registro guardado","Registro")
        if (rap==True):
            newid = mycol.count_documents({})
            if (newid!=0):
                newid = mycol.find_one(sort=[('id',-1)])["id"]
            id=newid+1
            self.cid.set(id)
            mydict= {'id':int(self.custid.get()),'Primer nombre':self.custnombre.get(),'Primer apellido':self.custapellido.get(),
                    'Edad':int(self.custedad.get()),'Cédula':self.cidentidad.get(),'Género':self.custgenero.get(),
                    'Discapacidad':self.custdiscapacidad.get(),'Dirección':self.custdireccion.get(),'Bono':float(self.custbono.get()),
                    'Emprende':self.custemprende.get()
                    }
            agregaUno = mycol.insert_one(mydict)
            self.creategrid(1)
            self.creategrid(0)


    def elimina (self):
        '''
        Método que permite eliminar un reegistro nuevo a la base de datos
        Atraves de la cédula que se valla a ingresar.
        '''
        rap=self.msgbox("Registro eliminado","Eliminar")
        if (rap==True):
            myquerry = {'id':int(self.custid.get())}
            mycol.delete_one(myquerry)
        self.creategrid(1)
        self.creategrid(0)


    def limpiar(self):
            '''
            Método que limpia los Entry de la interfaz gráfica dejando todo como nuevo.
            '''
            self.cnombre1.set('')
            self.capelli1.set('')
            self.cedad.set('')
            self.cidentidad.set('')
            self.cgenero.set('Elegir opción')
            self.cdiscapacidad.set('')
            self.cdireccion.set('Elegir opción')
            self.cbono.set('')
            self.cemprende.set('')

    def modifica (self):
        '''
            Método que permite modificar un reegistro nuevo a la base de datos
            Atraves de la cédula que se valla a ingresar.
        '''
        rap=self.msgbox("Registro modificado","Modificar")
        if rap == True:
            myquerry = {'id':int(self.custid.get())}
            newvalues = {"$set":{"Primer nombre":self.custnombre.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Primer apellido":self.custapellido.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Edad":self.custedad.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Cédula":self.custidentidad.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Género":self.custgenero.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Discapacidad":self.custdiscapacidad.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Dirección":self.custdireccion.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"bono":self.custbono.get()}}
            mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Emprende":self.custemprende.get()}}
            mycol.update_one(myquerry,newvalues)
            self.creategrid(1)
            self.creategrid(0)

    def __init__ (self):
        '''
        Método constructor de las interfaces gráficas.
        '''
        #Ventana principal.
        self.window = tk.Tk()
        self.window.title("Base de datos del sistema")
        self.window.geometry("810x600")
        self.window.config(bg="gray22")
        #Sub ventanas
        self.frame1 = Frame(self.window)
        self.frame1.grid(columnspan=14, column=0,row=0)
        self.frame2 = Frame(self.window, bg='#4779b2')
        self.frame2.grid(columnspan=14,column=0, row=1)
        self.frame4 = Frame(self.window, bg='#4779b2')
        self.frame4.grid(columnspan=14,column=0, row=3,pady=5)

        #-------------------------- Label y Entry del la interfaz --------------------------

        self.label=tk.Label(self.frame1, text = 'R E G I S T R O   D E   D A T O S',bg='gray22',fg='white', font=('Orbitron',15,'bold'))
        self.label.grid(column=0, row=0)

        self.label = tk.Label(self.frame2, text='Agregar Nuevos Datos',fg='gray90', bg ='#4779b2', font=('Rockwell',12,'bold'))
        self.label.grid(columnspan=3, column=0,row=0, pady=10)

        self.label = tk.Label(self.frame2, text='Nº',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=2)
        self.cid= tk.StringVar()
        self.custid = tk.Entry(self.frame2, textvariable=self.cid,width=21)
        self.custid.grid(column=2,row=2)
        self.custid.configure(state=tk.DISABLED)

        self.label = tk.Label(self.frame2, text='Nombre',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=3)
        self.cnombre1 = tk.StringVar()
        self.custnombre = tk.Entry(self.frame2, textvariable=self.cnombre1,width=21)
        self.custnombre.grid(column=2,row=3)


        self.label = tk.Label(self.frame2, text='Apellido',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=4)
        self.capelli1 = tk.StringVar()
        self.custapellido = tk.Entry(self.frame2, textvariable=self.capelli1,width=21)
        self.custapellido.grid(column=2,row=4)


        self.label = tk.Label(self.frame2, text='Edad',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=5)
        self.cedad = tk.StringVar()
        self.custedad = tk.Entry(self.frame2, textvariable=self.cedad,width=21)
        self.custedad.grid(column=2,row=5)

        self.label = tk.Label(self.frame2, text='Cédula', fg='white',bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=6)
        self.cidentidad = tk.StringVar()
        self.custidentidad = tk.Entry(self.frame2, textvariable=self.cidentidad,width=21)
        self.custidentidad.grid(column=2,row=6)

        self.label = tk.Label(self.frame2, text='Género',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=7)
        self.cgenero = tk.StringVar()
        self.custgenero = tk.Entry(self.frame2, textvariable=self.cgenero)
        self.cgenero.set('Elegir opcion')
        self.sexo=['Masculino','Femenino','LGBT']
        self.menu=tk.OptionMenu(self.frame2,self.cgenero,*self.sexo)
        self.menu.config(width=15, height=1,bg= "white")
        self.menu.grid(column=2,row=7)

        self.label = tk.Label(self.frame2, text='Discapacidad.',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=8)
        self.cdiscapacidad = tk.StringVar()
        self.custdiscapacidad = tk.Entry(self.frame2, textvariable=self.cdiscapacidad,width=21)
        self.custdiscapacidad.grid(column=2,row=8)

        self.label = tk.Label(self.frame2, text='Dirección',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=9)
        self.cdireccion = tk.StringVar(self.frame2)
        self.custdireccion = tk.Entry(self.frame2, textvariable=self.cdireccion)
        self.cdireccion.set("Elegir opcion")
        self.calles=[
            'Barrio bryan','Barrio las palmas','29 de mayo','km 23 via Quevdo','Luz de américa',
            'Santo domingo','Eloy Alfaro','Barrio Cricita','Valla vista','Lotizaciones Wilson Eraso',]
        self.menu=tk.OptionMenu(self.frame2,self.cdireccion,*self.calles)
        self.menu.config(width=15, height=1,bg= "white")
        self.menu.grid(column=2,row=9)


        self.label = tk.Label(self.frame2, text='Bono',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=10)
        self.cbono = tk.StringVar()
        self.custbono = tk.Entry(self.frame2, textvariable=self.cbono,width=21)
        self.custbono.grid(column=2,row=10)


        self.label = tk.Label(self.frame2, text='Emprede',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold'))
        self.label.grid(column=1,row=11)
        self.cemprende = tk.StringVar()
        self.custemprende = tk.Entry(self.frame2, textvariable=self.cemprende,width=21)
        self.custemprende.grid(column=2,row=11)

        self.creategrid(0)

        self.control = tk.Label(self.frame4, text = 'Controles',fg='white', bg ='#4779b2', font=('Rockwell',12,'bold'))
        self.control.grid(columnspan=4, column=0,row=0, pady=10,padx=0)

        self.savebtn = tk.Button(self.frame4,text='GUARDAR', font=('Arial',10,'bold'), bg='#8da9c9', command=self.guarda)
        self.savebtn.grid(column=0,row=1, pady=10,padx=0)

        self.limpia = tk.Button(self.frame4,text='LIMPIAR', font=('Arial',10,'bold'), bg='#8da9c9', command=self.limpiar)
        self.limpia.grid(column=1,row=1, pady=10,padx=0)

        self.savebtn = tk.Button(self.frame4,text='ELIMINAR', font=('Arial',10,'bold'), bg='#8da9c9', command=self.elimina)
        self.savebtn.grid(column=2,row=1, pady=10,padx=0)

        self.savebtn = tk.Button(self.frame4,text='MODIFICAR', font=('Arial',10,'bold'), bg='#8da9c9', command=self.modifica)
        self.savebtn.grid(columnspan=3,column=0,row=3, pady=10,padx=0)

        self.window.mainloop()

if __name__ == "__main__":
    BaseData()

    mainP()
