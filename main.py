from tkinter import Entry, Label, Frame, Tk, Button,ttk, Scrollbar, VERTICAL, HORIZONTAL,StringVar
import pymongo
import tkinter as tk
from tkinter import messagebox



class Registro(Frame):
    '''
    La clase registro permite hacer un interfaz gráfica de la modificación
    que puede reliazar un colaborar de la empresa.

     ATRIBUTOS
     ----------
         *args: tuple
             El principal uso de *args y **kwargs es en la definición de funciones.
             Ambos permiten pasar un número variable de argumentos a una función.
         **kwargs: dict
             El principal uso de *args y **kwargs es en la definición de funciones.
             Ambos permiten pasar un número variable de argumentos a una función.

         METODO
         -------
             __init__(self, master,*args, **kwargs):
                 Método constructor de la clase
             create_ventana(self):
                 Permite crear la interfaz grádica.
             msgbox(self,msg,titulobar):
                 Permiten enviar un mensaje de información
             def callback(self,event):
                 Muestra en pantalla los daton ingresados
             def creategrid(self,num):
                 Ayuda a eliminar agregar y modificar lo datos.
             def inserta(self):
                 Método que inserta los datos.
             def elimina (self):
                 Método que elimina los datos
             def modifica (self):
                 Método que modfica los datos
             limpiar_datos(self):
                 Limpia los datos en la pantalla.        
    '''
    def __init__(self, master,*args, **kwargs):
        '''
        Método constructor de la clase.

         PARAMETROS
         -----------
             *args: tuple
                 El principal uso de *args y **kwargs es en la definición de funciones.
                 Ambos permiten pasar un número variable de argumentos a una función.
             **kwargs: dict
                 El principal uso de *args y **kwargs es en la definición de funciones.
                 Ambos permiten pasar un número variable de argumentos a una función.

        '''
        super().__init__(master, *args, **kwargs)

        self.myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.mydb = self.myclient['Ciudadanos']
        self.mycol = self.mydb['Registrados']

        self.frame1 = Frame(master)
        self.frame1.grid(columnspan=2, column=0,row=0)
        self.frame2 = Frame(master, bg='#4779b2')
        self.frame2.grid(column=0, row=1)

        self.frame4 = Frame(master, bg='#4779b2')
        self.frame4.grid(column=0, row=3)

        self.nombre=StringVar()
        self.apellido=StringVar()
        self.edad=StringVar()
        self.cedula=StringVar()
        self.genero=StringVar()
        self.direccion=StringVar(master)
        self.discapa=StringVar()
        self.bono=StringVar()
        self.emprende=StringVar()
        self.create_ventana()

    def create_ventana(self):
        Label(self.frame1, text = 'R E G I S T R O   D E   D A T O S',bg='gray22',fg='white', font=('Orbitron',15,'bold')).grid(column=0, row=0)
        
        Label(self.frame2, text = 'Agregar Nuevos Datos',fg='gray90', bg ='#4779b2', font=('Rockwell',12,'bold')).grid(columnspan=2, column=0,row=0, pady=10)
        Label(self.frame2, text = 'Nombre',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=1, pady=4)
        Label(self.frame2, text = 'Apellido',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=2, pady=4)
        Label(self.frame2, text = 'Edad',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=3, pady=4)
        Label(self.frame2, text = 'Cédula', fg='white',bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=4, pady=4)
        Label(self.frame2, text = 'Género',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=5, pady=4)
        Label(self.frame2, text = 'Dirección',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=6, pady=4)
        Label(self.frame2, text = 'Discapa.',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=7, pady=4)
        Label(self.frame2, text = 'Bono',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=8, pady=4)
        Label(self.frame2, text = 'Emprede',fg='white', bg ='#4779b2', font=('Rockwell',11,'bold')).grid(column=0,row=9, pady=4)


        Entry(self.frame2,textvariable=self.nombre , font=('Arial',9)).grid(column=1,row=1, padx =4)
        Entry(self.frame2,textvariable=self.apellido , font=('Arial',9)).grid(column=1,row=2)
        Entry(self.frame2,textvariable=self.edad , font=('Arial',9)).grid(column=1,row=3)
        Entry(self.frame2,textvariable=self.cedula , font=('Arial',9)).grid(column=1,row=4)
        Entry(self.frame2,textvariable=self.genero , font=('Arial',9)).grid(column=1,row=5)
        self.direccion.set("Elegir opcion")
        calles=[
            'Barrio bryan','Barrio las palmas','29 de mayo','km 23 via Quevdo','Luz de américa',
            'Santo domingo','Eloy Alfaro','Barrio Cricita','Valla vista','Lotizaciones Wilson Eraso']
        self.menu=tk.OptionMenu(self.frame2,self.direccion,*calles)
        self.menu.config(width=15, height=1,bg= "white")
        self.menu.grid(column=1,row=6)
        Entry(self.frame2,textvariable=self.discapa , font=('Arial',9)).grid(column=1,row=7)
        Entry(self.frame2,textvariable=self.bono , font=('Arial',9)).grid(column=1,row=8)
        Entry(self.frame2,textvariable=self.emprende , font=('Arial',9)).grid(column=1,row=9)

       
        Label(self.frame4, text = 'Controles',fg='white', bg ='#4779b2', font=('Rockwell',12,'bold')).grid(columnspan=3, column=0,row=0, pady=10,padx=0)         
        Button(self.frame4,command= self.inserta, text='REGISTRAR', font=('Arial',10,'bold'), bg='#8da9c9').grid(column=0,row=1, pady=10,padx=0)
        Button(self.frame4,command = self.limpiar_datos, text='LIMPIAR', font=('Arial',10,'bold'), bg='#8da9c9').grid(column=1,row=1,pady=10,padx=0)        
        Button(self.frame4,command = self.elimina, text='ELIMINAR', font=('Arial',10,'bold'), bg='#8da9c9').grid(column=2,row=1, pady=10,padx=0)
        Button(self.frame4,command = self.modifica, text='MODIFICAR', font=('Arial',10,'bold'), bg='#8da9c9').grid(columnspan=3,column=0,row=3, pady=10,padx=0)

    '''Lista de parametros que se mostraran en la pantalla''' 
    lst = [('Nombre','Apellido','Edad','Cédula','Género','Discapa','Dirección','Bono','Emprende')]

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

    def callback(self,event):
        '''
        Sirve para dar las posiciones en la diferente columna del programa.

         PARAMETROS
         -----------
             event: any
                 
        '''
        li=[]
        li=event.widget._values
        self.nombre.set(self.lst(li[1])[1])
        self.apellido.set(self.lst(li[1])[3])
        self.edad.set(self.lst(self.li[1])[5])
        self.cedula.set(self.lst(li[1])[6])
        self.genero.set(self.lst(self.li[1])[8])
        self.discapa.set(self.lst(li[1])[9])
        self.direccion.set(self.lst(li[1])[10])
        self.bono.set(self.lst(li[1])[13])
        self.emprende.set(self.lst(li[1])[15])

    def obtener_fila(self, event):
        '''
        Método que permite obtener las filas de la interfaz gráfica.
        '''
        current_item = self.tabla.focus()
        if not current_item:
            return
        data = self.tabla.item(current_item)
        self.nombre_borar = data['values'][0]

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
        self.lst.clear()
        self.lst.append(['Nombre','Apellido','Edad','Cédula','Género','Discapa','Dirección','Bono','Emprende'])
        cursor = self.mycol.find({})
        for text_fromDB in cursor:
            self.nombre = str(text_fromDB['Primer nombre']).encode('utf_8').decode("utf_8")
            self.apellido = str(text_fromDB['Primer apellido']).encode('utf_8').decode("utf_8")
            self.edad = int(text_fromDB['Edad'])
            self.cedula = str(text_fromDB['Cédula']).encode('utf_8').decode("utf_8")
            self.genero =  str(text_fromDB['Género']).encode('utf_8').decode("utf_8")
            self.discapa = str(text_fromDB['Discapacidad']).encode('utf_8').decode("utf_8")
            self.direccion = str(text_fromDB['Dirección']).encode('utf_8').decode("utf_8")
            self.bono = float(text_fromDB['Bono'])
            self.emprende = str(text_fromDB['Emprende']).encode('utf_8').decode("utf_8")
            self.lst.append([self.nombre,self.apellido,self.edad,self.cedula,self.genero,
                            self.discapa,self.direccion,self.bono,self.emprende])
        
        for interacion in range(len(self.lst)):
            for itera in range(len(self.lst[0])):
                mgrid = tk.Entry(self.frame2,width=10)
                mgrid.insert(tk.END,self.lst[interacion][itera])
                mgrid._values = mgrid.get(),interacion
                mgrid.grid(row=(interacion+1), column=(itera+2))
                mgrid.bind("<Button-1>", self.callback)

        if (num==1):
            for label in self.frame2.grid_slaves():
                if (int(label.grid_info()("row")) > 6):
                    label.grid_forget()

    def inserta(self):
        '''
        Método que permite insertar un reegistro nuevo a la base de datos
        Atraves de los campos que se vallan a ingresar.
        '''
        rap=self.msgbox("Registro guardado","Registro")
        if (rap==True):
            mydict= {'Primer nombre':self.nombre.get(),'Primer apellido':self.apellido.get(),
                    'Edad':int(self.edad.get()),'Cédula':self.cedula.get(),'Género':self.genero.get(),
                    'Discapacidad':self.discapa.get(),'Dirección':self.direccion.get(),'Bono':float(self.bono.get()),
                    'Emprende':self.emprende.get()
                    }
            self.mycol.insert_one(mydict)
            self.creategrid(1)
            self.creategrid(0)

    def elimina (self):
        '''
        Método que permite eliminar un reegistro nuevo a la base de datos
        Atraves de la cédula que se valla a ingresar.
        '''
        rap=self.msgbox("Registro eliminado","Eliminar")
        if (rap==True):
            self.myquerry = {'Cédula':self.cedula.get()}
            self.mycol.delete_one(self.myquerry)
        self.creategrid(1)
        self.creategrid(0)

    def modifica (self):
        '''
        Método que permite modificar un reegistro nuevo a la base de datos
        Atraves de la cédula que se valla a ingresar.
        '''
        self.rap=self.msgbox("Registro modificado","Modificar")
        if self.rap == True:
            myquerry = {'Cédula':self.cedula.get()}
            newvalues = {"$set":{"Primer nombre":self.nombre.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Primer apellido":self.apellido.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"edad":self.edad.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Cédula":self.cedula.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Género":self.genero.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Discapacidad":self.discapa.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Dirección":self.direccion.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"bono":self.bono.get()}}
            self.mycol.update_one(myquerry,newvalues)

            newvalues = {"$set":{"Emprende":self.emprende.get()}}
            self.mycol.update_one(myquerry,newvalues)
            self.creategrid(1)
            self.creategrid(0)

    def limpiar_datos(self):
        '''
        Método que limpia los Entry de la interfaz gráfica dejando todo como nuevo.
        '''
        self.tabla.delete(*self.tabla.get_children())
        self.nombre.set('')
        self.apellido.set('')
        self.edad.set('')
        self.cedula.set('')
        self.genero.set('')
        self.discapa.set('')
        self.direccion.set('')
        self.bono.set('')
        self.emprende.set('')

def mainP():
    '''
    Procedimiento que permite crear la ventana principal
    de la interfaz gráfica.
    '''
    ventana = Tk()
    ventana.wm_title("Registro de Datos")
    ventana.config(bg='gray22')
    ventana.geometry('1205x530')
    app = Registro(ventana)
    app.mainloop()

if __name__=="__main__":
    '''Llamando a mein principal.'''
    mainP()