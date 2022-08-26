
'''
Librería que permirá generár archivos pdf
from fpdf import FPDF
Librería que va a ser usada para devolver la fecha actual.
import datetime
Librería exportada particularmente.
from parametrosPDF import *
'''
from fpdf import FPDF
import datetime
from parametrosPDF import *

class PDF(FPDF):
    '''
    La clase PDF herada del objeto FPDF los atributos necesarios
    para poder gener archivos en formato PDF.

     ATRIBUTOS
     ----------
         Son heredados de la clase base.

     METODOS
     --------
         header(self):
             Método que contiene la imagen y el título principal.
             ademas de incluir la fecha actual.
         footer(self):
             Método que configura el pié de página del archivo PDF
    '''
    def header(self):
        '''
        Método que contiene la imagen y el título principal.
        ademas de incluir la fecha actual.
        '''
        self.image('credito.png',x = 60, y = 10, w = 60, h = 36)

        self.set_font('Arial', '', 15)

        tcol_set(self, 'blue')
        tfont_size(self,25)
        tfont(self,'B')
        self.cell(w = 0, h = 20, txt = 'Turno Nº 001', border = 0, ln=1,align = 'R', fill = 0)

        tfont_size(self,12)
        tcol_set(self, 'black')
        tfont(self,'BI')
        self.cell(w = 0, h = 10, txt = ('Generado el '+datetime.date.today().strftime('%Y/%m/%d')), border = 0, ln=2,align = 'R', fill = 0)

        self.ln(5)

    # Pie de página
    def footer(self):
        '''
        Método que configura el pié de página del archivo PDF
        además de incluir un número de página y el formato de letra.
        '''
        # Posición a 1,5 cm de la parte inferior
        self.set_y(-20)

        # Arial cursiva 8
        self.set_font('Arial', 'I', 12)

        # Número de página
        self.cell(w = 0, h = 10, txt =  '[Pág ' + str(self.page_no()) + '/{nb}]',border = 0,align = 'R', fill = 0)   


'''Lista adicional de datos'''
lista_datos = (
    (1, 'Carlos', '2300324157', '2023-02-25'),
    (2, 'Jose', '1710445574', '2023-03-12'),
    (3, 'Limberto', '2314587895', '2023-01-31'),
    (4, 'Luz', '2305487895', '2023-02-15'),
    (5, 'Anahí', '2336521478', '2023-02-23'),
)#*8


pdf = PDF(orientation = 'P', unit = 'mm', format='A4') 
pdf.alias_nb_pages()

pdf.add_page()

# TEXTO
pdf.set_font('Arial', '', 15) 


# 1er encabezado ----

bcol_set(pdf, 'green')
tfont_size(pdf,15)
tfont(pdf,'B')
pdf.multi_cell(w = 0, h = 15, txt = 'Información del turno', border = 0, align = 'C', fill = 1)
tfont(pdf,'')


h_sep = 15
pdf.ln(3)
tfont_size(pdf,12)

# fila 1 --

tcol_set(pdf, 'gray')
pdf.cell(w = 45, h = h_sep, txt = 'Nombre:', border = 0, align = 'R', fill = 0)

tcol_set(pdf, 'black')         
pdf.cell(w = 45, h = h_sep, txt = "Marco", border = 0, align = 'L', fill = 0)

tcol_set(pdf, 'gray')
pdf.cell(w = 45, h = h_sep, txt = 'Cédula:', border = 0, align = 'R', fill = 0)

tcol_set(pdf, 'black') 
pdf.multi_cell(w = 0, h = h_sep, txt = '2300521914', border = 0, align = 'L', fill = 0)


# fila 2 --
tcol_set(pdf, 'gray')
pdf.cell(w = 45, h = h_sep, txt = 'Apellido:', border = 0, align = 'R', fill = 0)

tcol_set(pdf, 'black')
pdf.cell(w = 45, h = h_sep, txt = 'Olmedo', border = 0,align = 'L', fill = 0)

tcol_set(pdf, 'gray')
pdf.cell(w = 45, h = h_sep, txt = 'Fecha de solicitud:', border = 0,  align = 'R', fill = 0)

tcol_set(pdf, 'black')
pdf.multi_cell(w = 0, h = h_sep, txt = '2023/02/14', border = 0,align = 'L', fill = 0)

# fila 3 --
tcol_set(pdf, 'gray')
pdf.cell(w = 45, h = h_sep, txt = 'Dirrección:', border = 0, align = 'R', fill = 0)

tcol_set(pdf, 'black')
pdf.cell(w = 45, h = h_sep, txt = 'Lotizaciones Wilson Eraso', border = 0,align = 'L', fill = 0)

tcol_set(pdf, 'gray')
pdf.cell(w = 45, h = h_sep, txt = 'Hora:', border = 0, align = 'R', fill = 0)

tcol_set(pdf, 'black')
pdf.multi_cell(w = 0, h = h_sep, txt = '09:15', border = 0,align = 'L', fill = 0)




pdf.ln(15)
# tabla ----

bcol_set(pdf, 'green')
tfont_size(pdf,15)
tfont(pdf,'B')
pdf.cell(w = 0, h = 15, txt = 'Otros turnos', border = 0,ln = 2, align = 'C', fill = 1)
tfont(pdf,'')

tfont_size(pdf,13)
bcol_set(pdf, 'blue')

pdf.cell(w = 20, h = 10, txt = 'Nº', border = 0, align = 'C', fill = 1)
pdf.cell(w = 40, h = 10, txt = 'Nombre', border = 0, align = 'C', fill = 1)
pdf.cell(w = 70, h = 10, txt = 'Cédulas', border = 0, align = 'C', fill = 1)
pdf.multi_cell(w = 0, h = 10, txt = 'Fecha de solicitud', border = 0, align = 'C',fill = 1)


tfont_size(pdf,12)
dcol_set(pdf, 'blue')
tcol_set(pdf, 'gray')
pdf.rect(x= 10, y= 60, w= 190, h= 53)
c = 0

'''Ciclo for que imprimirá la lista adicional de datos declarada anteriormente.'''
for datos in lista_datos:

    c+=1
    if(c%2==0):bcol_set(pdf, 'gray2')
    else:bcol_set(pdf, 'white')

    pdf.cell(w = 20, h = 10, txt = str(datos[0]), border = 'TBL', align = 'C', fill = 1)
    pdf.cell(w = 40, h = 10, txt = datos[1], border = 'TB', align = 'C', fill = 1)
    pdf.cell(w = 70, h = 10, txt = datos[2], border = 'TB', align = 'C', fill = 1)
    pdf.multi_cell(w = 0, h = 10, txt = datos[3], border = 'TBR', align = 'C', fill = 1)

