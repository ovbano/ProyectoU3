def diccionario_colores(color): 
    '''
    Funcion que permite dar colores para generar 
    un pdf más auténtico.

     RETORNA
     --------
         return colores[color]
    '''
    colores = {
        'black' : (0,0,0), 
        'white' : (255,255,255),
        'green' : (50,140,200),
        'blue' : (200,95,90),
        'red': (239,71,71),
        'rose':(100,100,100),
        'gray':(103,103,103),
        'gray2':(233,233,233),
        }
    return colores[color]

def dcol_set(hoja, color):
    '''
    La función dcol_set distribuye los colores para generar el PDf
    '''
    cr, cg, cb = diccionario_colores(color)
    hoja.set_draw_color(r= cr, g = cg, b= cb)
    
def bcol_set(hoja,color):
    '''
    La función bcol_set distribuye los colores para generar el PDf
    '''
    cr, cg, cb = diccionario_colores(color)
    hoja.set_fill_color(r= cr, g = cg, b= cb)

def tcol_set(hoja, color):
    '''
    La función tcol_set distribuye los colores para generar el PDf
    '''
    cr, cg, cb = diccionario_colores(color)
    hoja.set_text_color(r= cr, g = cg, b= cb)
    
def tfont_size(hoja, size):
    '''
    
    '''
    hoja.set_font_size(size)

def tfont(hoja, estilo, fuente='Arial'):
    '''
    La función tfont Permite dar la funente de la lecha en Arial.
    '''
    hoja.set_font(fuente, style=estilo)