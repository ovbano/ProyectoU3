import tkinter as tk
import generic as utl


class MasterPanel:
    '''
    La clase MasterPanel permite mostrar el panel principal del login de usuario

     METODO
     --------
         __init__(self):
             Método constructor que permite crear el panel.
    '''         
    def __init__(self):   
        '''
        Método que construye el panel
        '''     
        self.ventana = tk.Tk()                             
        self.ventana.title('Master panel')
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()                                    
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)            
        
        logo =utl.leer_imagen("credito.png", (200, 200))
                        
        label = tk.Label( self.ventana, image=logo,bg='#3a7ff6' )
        label.place(x=0,y=0,relwidth=1, relheight=1)
        
        self.ventana.mainloop()

