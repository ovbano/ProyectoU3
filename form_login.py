import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import pymongo
from form_master import *
from main import *

class App:
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['Ciudadanos']
    mycol = mydb['Colaboradores']
    '''
    La clase App Permitirá realizar un login

     METODOS
         verificar(self):
             Verifica que los usuarios y contraseña sean los correctos
         __init__(self):
             Método init construye las ventanas y demás arreglos para 
             la interfaz.
    '''
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
        self.result=messagebox.askokcancel(title=titulobar,message=msg)
        return self.result
    
    def modifica(self):
        mainP=BaseData()

        return mainP

    def conecDBusaer (self):
        '''
        Permite hallar el usuario correspondiente en la base de datos mongo

         RETORNA
         --------
             return user
        '''
        myquerry={'Correo':self.usuario.get()}
        user = self.mycol.find_one(myquerry)
        return user

    def conecDBpass (self):
        '''
        Permite hallar la contraseña correspondiente en la base de datos mongo

         RETORNA
         --------
             return passw 
        '''
        myquerry={'Cedula':self.password.get()}
        passw = self.mycol.find_one(myquerry)
        return passw 

    def verificar(self):
        '''
        Permite validad el correcto ingreso de la contraseña y el usuario.
        '''       
        if(self.conecDBusaer() and self.conecDBpass()) :
            self.ventana.destroy()
            self.modifica()
        else:
            messagebox.showerror(message="El usuario o la contraseña no es correcta",title="Mensaje")           

    def __init__(self):  
        '''
        Crea la parte parte de la interfaz del proyecto.
        '''      
        self.ventana = tk.Tk()                             
        self.ventana.title('Inicio de sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        
        #frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form
        
        #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion",font=('Times', 30), fg="#666a88",bg='#fcfcfc',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14) ,fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14),fg="#666a88",bg='#fcfcfc' , anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill,text="Iniciar sesion",font=('Times', 15,BOLD),bg='#3a7ff6', bd=0,fg="#fff",command=self.verificar)
        inicio.pack(fill=tk.X, padx=20,pady=20)        
        inicio.bind("<Return>", (lambda: self.verificar()))
        self.ventana.mainloop()

if __name__ == "__main__":

    #Instanciando la clase App para logiar al usuario
    App()
