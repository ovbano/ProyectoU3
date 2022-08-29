'''Librería, módulos o bibliotecas importadas tanto internamente como externamente'''
import datetime
import tkinter as tk
import pymongo
from tkcalendar import Calendar, DateEntry 
from tkinter import *
from tkinter import messagebox
import requests 
import os
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC, JUL
from holidays.holiday_base import HolidayBase
from crarPDF import *
from Acreditate import *
from form_login import App

class HolidayEcuador(HolidayBase):
    """
    Una clase para representar un feriado en Ecuador por provincia (HolidayEcuador)
    Su objetivo es determinar si un
    fecha específica es u nas vacaciones lo más rápido y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase HolidayBase)
    ----------
    prov: str
        código de provincia según ISO3166-2
    Métodos
    -------
    __init__(self, plate, fecha, tiempo, online=False):
        Construye todos los atributos necesarios para el objeto HolidayEcuador.
    _poblar(uno mismo, año):
        Devoluciones si una fecha es feriado o no
    """     
    # Códigos ISO 3166-2 para las principales subdivisiones,
    # provincias llamadas
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO añadir más provincias

    def __init__(self, **kwargs):
        """
        Construye todos los atributos necesarios para el objeto HolidayEcuador
        """         
        self.country = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        Comprueba si una fecha es feriado o no
        
        Parámetros
        ----------
        año: calle
            año de una fecha
        Devoluciones
        -------
        Devuelve verdadero si una fecha es un día festivo, de lo contrario, se muestra como verdadero.
        """
        # Festividades santo domingo
        self[datetime.date(year, JUL, 3)] = "Cantonalización de Santo Domingo" 
        self[datetime.date(year, NOV, 6)] = "Provincialización de Santo Domingo"

        # Festividades parroquiales 'Luz de américa'
        self[datetime.date(year, AUG, 2)] = "Fiestas patronales"

        # Día de Año Nuevo 
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(year, DEC, 25)] = "Navidad [Christmas]"
        
        # semana Santa
        self[easter(year) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(year)] = "Día de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(year) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(year) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Día laboral
        trabajo = "Día Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if year > 2015 and datetime.date(year, MAY, 1).weekday() in (5,1):
            self[datetime.date(year, MAY, 1) - datetime.timedelta(days=1)] = trabajo
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif year > 2015 and datetime.date(year, MAY, 1).weekday() == 6:
            self[datetime.date(year, MAY, 1) + datetime.timedelta(days=1)] = trabajo
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # se moverá al viernes de esa semana
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, MAY, 1) + rd(weekday=FR)] = trabajo
        else:
            self[datetime.date(year, MAY, 1)] = trabajo      
        
        # Primer Grito de Independencia, las reglas son las mismas que el día del trabajo
        grito = "Primer Grito de la Independencia [First Cry of Independence]"
        if year > 2015 and datetime.date(year, AUG, 10).weekday() in (5,1):
            self[datetime.date(year, AUG, 10)- datetime.timedelta(days=1)] = grito
        elif year > 2015 and datetime.date(year, AUG, 10).weekday() == 6:
            self[datetime.date(year, AUG, 10) + datetime.timedelta(days=1)] = grito
        elif year > 2015 and  datetime.date(year, AUG, 10).weekday() in (2,3):
            self[datetime.date(year, AUG, 10) + rd(weekday=FR)] = grito
        else:
            self[datetime.date(year, AUG, 10)] = grito       
        
        # Independencia de Guayaquil, las reglas son las mismas que el día del trabajo
        independencia = "Independencia de Guayaquil [Guayaquil's Independence]"
        if year > 2015 and datetime.date(year, OCT, 9).weekday() in (5,1):
            self[datetime.date(year, OCT, 9) - datetime.timedelta(days=1)] = independencia
        elif year > 2015 and datetime.date(year, OCT, 9).weekday() == 6:
            self[datetime.date(year, OCT, 9) + datetime.timedelta(days=1)] = independencia
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, OCT, 9) + rd(weekday=FR)] = independencia
        else:
            self[datetime.date(year, OCT, 9)] = independencia        
        
        # Día de Muertos
        fieles = "Día de los difuntos [Day of the Dead]" 
        if (datetime.date(year, NOV, 2).weekday() == 5 and  datetime.date(year, NOV, 3).weekday() == 6):
            self[datetime.date(year, NOV, 2) - datetime.timedelta(days=1)] = fieles    
        elif (datetime.date(year, NOV, 3).weekday() == 2):
            self[datetime.date(year, NOV, 2)] = fieles
        elif (datetime.date(year, NOV, 3).weekday() == 3):
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = fieles
        elif (datetime.date(year, NOV, 3).weekday() == 5):
            self[datetime.date(year, NOV, 2)] =  fieles
        elif (datetime.date(year, NOV, 3).weekday() == 0):
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = fieles
        else:
            self[datetime.date(year, NOV, 2)] = fieles
            
        # Fundación de Quito, aplica solo para la provincia de Pichincha,
        # las reglas son las mismas que el día del trabajo
        Fundacion = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if year > 2015 and datetime.date(year, DEC, 6).weekday() in (5,1):
                self[datetime.date(year, DEC, 6) - datetime.timedelta(days=1)] = Fundacion
            elif year > 2015 and datetime.date(year, DEC, 6).weekday() == 6:
                self[(datetime.date(year, DEC, 6).weekday()) + datetime.timedelta(days=1)] =Fundacion
            elif year > 2015 and  datetime.date(year, DEC, 6).weekday() in (2,3):
                self[datetime.date(year, DEC, 6) + rd(weekday=FR)] = Fundacion
            else:
                self[datetime.date(year, DEC, 6)] = Fundacion


class PersonaAcreditada:
    """
    La clase persona bono servirá para identificar si una persona es beneficiaria
    al bono de desarrollo humano que entrega el gobiendo nacional juntos con el 
    Ministerio de Inclusión Económica y Socia:
    http://www.ecuadorlegalonline.com/consultas/consultar-si-cobro-el-bono-de-emergencia-del-mies/
    ...
     ATRIBUTOS
     -----------
             cedula:str
                 Valor numérico que representa el la identidad ciudadana de un persona
             fecha:str
                Fecha en la que el usuario desee retirar su crédito.
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             hora: str
                 Tiempo en se permiten el servicio de la adquisición del bono
                 esta siguiendo el formato
                 HH:MM: por ejemplo, 08:35, 19:30
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos
    Methods
    -------
     __init__(self, cedula, fecha, hora, online=False):
         Este método sive para construir todo los atributos correspondientes al 
         objeto personaBono
     cedula(self):
         Obtiene el valor del atributo de cédula
     cedula(self, value):
         Establece el valor del atributo de la cédula
     fecha(self):
         Obtiene el valor del atributo de fecha
     fehca(self, value):
         Establece el valor del atributo de la fecha
     hora(self):
         Obtiene el valor del atributo de hora
     hora(self, value):
         Establece el valor del atributo de la hora
     encontrar_día(self, fecha):
         Devuelve el día a partir de la fecha: por ejemplo, Jueves
     es_tiempo_descanso(self, check_time):
         Returns True if provided time is inside the forbidden peak hours, otherwise False
     esFeriado:
         Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo
         en Ecuador, de lo contrario, False
     evaluar(self):
         Devuelve True si una persona cumple con todos los prámetros para la adquisición
         del crédito al bono de desarrollo humano.
    """ 
    # Dias de la semana
    days = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]

    # Restricciones para los día segun el ultimo dígito de la cédula.
    restrictions = {
     "LUNES": [1, 2],
     "MARTES": [3, 4],
     "MIERCOLES": [5, 6],
     "JUEVES": [7, 8],
     "VIERNES": [9, 0],
     "SABADO": [],
     "DOMINGO": []}


    def __init__(self, cedula, fecha, hora, online=False):
        """
        Construye todos los atributos necesarios para la clase..
        
         PARAMETROS
         ----------
             cedula:str
                 Valor numérico que representa el la identidad ciudadana de un persona
             fecha:str
                 Fecha en la que el usuario desee retirar su crédito.
                 Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             hora: str
                 Tiempo en se permiten el servicio de la adquisición del bono
                 esta siguiendo el formato
                 HH:MM: por ejemplo, 08:35, 19:30
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos              
        """                
        self.cedula = cedula
        self.fecha = fecha
        self.hora = hora
        self.online = online


    @property
    def cedula(self):
        """Obtiene el valor del atributo de cedula"""
        return self._cedula

    @cedula.setter
    def cedula(self, value):
        """
        Establece el valor del atributo cedula
         Parámetros
         ----------
             valor: cadena de carácteres
                 El valor del atributo cédula debe darse en forma de cadena de carácteres
        
         RETORNA
         ------
             ValorError 
                 Si la cadena de valor cédula no tiene el siguiete 
                 formato: XXXXXXXXXX.
                 Donde X son los diez numeros correspondientes a la cédula de cuidadanía
        """
        if not re.match('^[0-9]{10}$', value):
            raise ValueError(
                'La cédula debe tener el siguiente formato: XXXXXXXXXX, donde X son los diez números correspondientes a la cédula de cuidadanía')
        self._cedula = value


    @property
    def fecha(self):
        """Obtiene el valor del atributo de fecha"""
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        """
        Establece el valor del atributo de fecha
         Parámetros
         ----------
             valor: cadena de carácteres
                 El valor del atributo cédula debe darse en forma de cadena de carácteres
        
         RETORNA
         ------
             ValorError
                 Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021/04/02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            raise ValueError('La fecha debe tener el siguiente formato: AAAA/MM/DD (por ejemplo: 2021/04/02)') from None
        self._fecha = value
        

    @property
    def hora(self):
        """Obtiene el valor del atributo hora"""
        return self._hora


    @hora.setter
    def hora(self, value):
        """
        Establece el valor del atributo de hora
         Parameters
         ----------
             value : str
                 Valor que permite determinar si el horario es el correcto o no
        
         Raises
         ------
             ValueError
                 Si la cadena de valor no tiene el formato HH:MM (por ejemplo, 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'La hora debe tener el siguiente formato: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._hora = value


    def __encontrar_dia(self, fecha):
        """
        Encuentra el día a partir de la fecha: por ejemplo, jueves
        
         Parámetros
         ----------
             fecha: str
                 Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        
         Devoluciones
         -------
             Devuelve el día a partir de la fecha como una cadena
        """        
        dia = datetime.datetime.strptime(fecha, '%Y/%m/%d').weekday()
        return self.days[dia]


    def __es_tiempo_descanso(self, check_hora):
        """
        Método que comprueba si el tiempo proporcionado está dentro de las horas laborables,
        donde las horas laborales son: 07:30 - 12:00 y 13:00 - 16:30
        
         PARAMETRO
         ----------
             check_hora : str
                 Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        
         RETORNA
         -------
             Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
        """          
        tiempo = datetime.datetime.strptime(check_hora, '%H:%M').time()
        return ((tiempo >= datetime.time(7, 30) and tiempo <= datetime.time(11, 59)) or
                (tiempo >= datetime.time(13, 00) and tiempo <= datetime.time(16, 30)))


    def __es_feriado(self, fecha, online):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador.
        si online == Verdadero, utilizará una API REST, de lo contrario, generará los días 
        festivos del año examinado
        
         Parámetros
         ----------
             fecha: str
                 Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos
        
         RETORNA
         -------
             Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
        """          
        y, m, d = fecha.split('/')

        if online:
            # abstractapi Holidays API, free version: 1000 requests per month
            # 1 request per second
            # retrieve API key from enviroment variable
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # if there is no holiday we get an empty array
                return False
            # Fix Maundy Thursday incorrectly denoted as holiday
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = HolidayEcuador(prov='EC-P')
            return fecha in ecu_holidays


    def evaluar(self):
        """
        Comprueba si una persona es beneficiaria al crédito del bono de desarrollo
        humano según los parametros ingresados.
        http://www.ecuadorlegalonline.com/consultas/credito-de-desarrollo-humano/
         Devoluciones
         -------
             Devoluciones Verdadero si el persona es puede recibir el crédito en la
             hora, fecha y según el ultimo dígito de su cédula, en tal día.
        """
        # Comprobar si la fecha es un día festivo
        if self.__encontrar_dia(self.fecha):
            return True

        # Consultar 
        # o si se utilizan sólo dos letras
        if self.cedula[1] in 'AUZEXM' or len(self.cedula.split('-')[0]) == 2:
            return True

        # Compruebe si el tiempo esta dentro de las horas laborables propuestas.
        if not self.__es_tiempo_descanso(self.hora):
            return True

        day = self.__es_feriado(self.fecha)  # Buscar el día de la semana a partir de la fecha

        # Verifique si el último dígito de la cédula no está restringido en este día en particular
        if int(self.cedula[-1]) not in self.restrictions[day]:
            return True
        return False
  
  
class FiestasEcuador(PersonaAcreditada):

    '''
    La clase Credito(PersonaBono) sirve para identidicar si un usuario que sea beneficiario al bono
    de desarrollo humano puede recibir el crédito que ofrece el gobierno para las familias que esten
    emprendiendo algún tipo de negocio y poder reacctivar su condición económica.
    http://www.ecuadorlegalonline.com/consultas/credito-de-desarrollo-humano/

     ATRIBUTOS
     ----------
         -HEREDA DE LA CALSE BASE (PersonaBono).
         -------------------------------------------
     METODOS
     --------- 
         fecha (uno mismo):
             Obtiene el valor del atributo de fecha
         fecha (uno mismo, value):
             Establece el valor del atributo de fecha
             Devuelve el día a partir de la fecha: por ejemplo, miércoles
         determinarFecha:
             Enceutnra la el día apartir de la fecha digitada
         validarCedula:
             Valida la cédula segun el ultimo dígito su su numeración
         esFeriado:
             Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo
             en Ecuador, de lo contrario, False
        
    '''

    def __init__(self,fecha, online=False):
        '''
        Método constructor de la clase
        
         Parametros
         -----------
             fecha: str
                 Fecha ingresada por el usuario
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos 
        '''
        self.fecha=fecha
        self.online=online

    @property
    def fecha(self):
        """Obtiene el valor del atributo de fecha"""
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        """
        Establece el valor del atributo de fecha

         Parámetros
         ----------
             valor: cadena de carácteres
                 El valor del atributo cédula debe darse en forma de cadena de carácteres
        
         RETORNA
         ------
             ValorError
                 Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021/04/02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            raise ValueError('La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021/04/02)') from None
        self._fecha = value

    def determinarFecha(self,fecha):
        '''
        Método que determina un día apartir de la fecha ingresada.
         
         PARAMETROS
         -----------
             fecha: str
                 Fecha ingresada por el usuario

         RETORNA
         --------
             day = datetime.datetime.strptime(fecha, '%Y/%m/%d').weekday()
                 return self.days[day]
        '''
        day = datetime.datetime.strptime(fecha, '%Y/%m/%d').weekday()
        return self.days[day]

    def validarCedula (self):
        '''
        Método que permite validar la cédula ingresada por el usuario 
        según los parámetros establecidos.

         RETOTNA
         --------
             if int(self.cedula[-1]) not in self.restrictions[day]:
                 return True
        '''
        day = self.determinarFecha(self.fecha)  # Buscar el día de la semana a partir de la fecha

        # Verifique si el último dígito de la cédula no está restringido en este día en particular
        if int(self.cedula[-1]) not in self.restrictions[day]:
            return True

    def es_feriado(self, fecha, online):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador.
        si online == Verdadero, utilizará una API REST, de lo contrario, generará los días festivos del año examinado
        
         Parámetros
         ----------
             fecha: str
                 Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
             online: booleano, opcional
                 si en línea == Verdadero, se utilizará la API de días festivos abstractos
        
         RETORNA
         -------
             Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
        """            
        y, m, d = fecha.split('/')

        if online:
            # API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
            # 1 solicitud por segundo
            # recuperar la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave de API.
                raise requests.HTTPError(
                    'Falta la clave API. Guarde su clave en la variable de entorno HOLIDAYS_API_KEY')
            if response.content == b'[]':  # si no hay vacaciones, obtenemos una matriz vacía
                return False
            # Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['nombre'] == 'Jueves Santo':
                return False
            return True
        else:
            ecu_holidays = HolidayEcuador(prov='EC-P')
            return fecha in ecu_holidays

    def validacionFeriado(self):
        '''
        Método que permite identificar si hay un día festivo

         RETORNA
             if self.es_feriado(self.fecha, self.online):
                 return True
        '''
        # Comprobar si la fecha es un día festivo
        if self.es_feriado(self.fecha, self.online):
            return True


def es_tiempo_descanso(check_hora):
        """
        Función comprueba si el tiempo proporcionado está dentro de las horas laborables,
        donde las horas laborales son: 07:30 - 12:00 y 13:00 - 16:30
        
         PARAMETRO
         ----------
             check_hora : str
                 Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        
         RETORNA
         -------
             Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
        """           
        t = datetime.datetime.strptime(check_hora, '%H:%M').time()
        return ((t >= datetime.time(7, 30) and t <= datetime.time(11, 59)) or
                (t >= datetime.time(13, 00) and t <= datetime.time(16, 30)))

def validarhora (hora):
    '''
    Procedimiento que determina si un horario esta dentro de las hora laborables
    las cuales son establecidas anteriormente.

     PARAMETROS
     -----------
         hora : str
             Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15

     DEVUELVE
     -----------
         Devuelve un condicional con mensaje que muestran si la hora esta o no
         registrada.
    '''
    if es_tiempo_descanso(hora):

        messagebox.showinfo("Horario","Hora registrada")
    else:
        messagebox.showinfo(
            "Error", "Esta es hora de descanso los horario de labor son de 7:30 a 12:00 y de 13:00 a 16:00")


def validarFecha(fecha):
    '''
    Procedimiento que permite determinar si un fecha es día festivo o feriado
    establecidos en la clase FiestasEcuador.

     PARAMETRO
     ----------
         fecha: str
             Fecha en la que la persona desee apartar un turno.
         online: bool
             si en línea == Verdadero, se utilizará la API de días festivos abstractos
         fiesta: class
             Instancia de la clase FiestasEcuador 

     Devuelve
     ----------
         Devuelve un condicional el cual tiene un retorno de True si se cumple con 
         el método validacionFeriado de la clase FiestasEcuador
    '''
    online=False
    fiestas=FiestasEcuador(fecha, online)
    if fiestas.validacionFeriado():
        return True

    
def determiaDia (fecha):
    '''
    Función que obtiene el día apartir de una lista de todos los días.
    Además cumple con un formto de ingreso a la fecha.
    
     PARAMETROS
     -----------
         fecha: str
             Fecha en la que la persona desee apartar un turno.
         days: array
             Lista de los día de la semana
         day: class
             Permite obtener el formato para ingreso de la fecha

     RETORNO
     -----------
         Devuelve un dia espeficico apartir de la fecha ingresada.
    '''
    days = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
    day = datetime.datetime.strptime(fecha, '%Y/%m/%d').weekday()
    return days[day]

def validarDia (fecha):
    '''
    Función que permite restringir los día fines de semana mediante la fecha
    ingresada por el usuario.

     PARAMETROS
     -----------
         fecha: str
             Fecha en la que la persona desee apartar un turno.
         dia: función
             Corresponde a una funcion que permite determinar un el dia através
             de una lista, cumpliendo con un formato de fecha específico.
             
     RETORNO
         Devuelve true si los el dia apartir de la fecha cae un SABADO o DOMINGO.
    '''
    dia=determiaDia(fecha)
    if (dia == 'SABADO' or dia == 'DOMINGO'):
        return True   
    
def fechavalidada (fecha):
    '''
    Procedimiento que permite identificar si una fecha es o no feriado.
    Además de identificar el día apartir de la fecha ingresada.

     PARAMETROS
     -----------
         fecha: str
             Fecha en la que la persona desee apartar un turno.
    
     Devuelve
     ---------
         Devuenve un condicional True si la fecha ingresada corresponde a un día festivo
         o si corresponde a un día fin de semana. False si la fecha corresponde a un día
         laborable cotidiano.
    '''
    if (validarFecha(fecha) or validarDia(fecha)):
    
        messagebox.showerror(
            "Información","Esta fecha corresponde a un fecha festivo o a un día fin de semana. Este dia no se labora.")
    else:
        messagebox.showinfo("Información","Fecha registrada con exito")


def validadCedula(cedula):
    '''
    Función que permite enviar un mensaje en un ventana de interfaz gráfica
    Sobre la validación de la cédula.
    
     PARAMETRO
     ---------
         cedula:str
             Valor numérico que representa el la identidad ciudadana de un persona
     
     RETORNA
     ---------
         Retorna un ciclo for con los resultados de buscar la cédula en la base de datos mongoDB
    '''
    resultado = mycoleccion.find({"Cédula":cedula})
    for resul in (resultado):
        if (resul not in mycoleccion.find({})):
            messagebox.showerror(
                "Información","")
        else:
            messagebox.showinfo("Información","Se encontró su número de cédula")
    
def generarPDF (cedula,fecha,hora):
    '''
    Función que Permite generar un archivo pdf con los paramétros ingresados por el usuario

     PARAMETROS
     -----------
         cedula:str
             Valor numérico que representa el la identidad ciudadana de un persona
         fecha: str
             Fecha en la que la persona desee apartar un turno.
         hora : str
             Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15

     RETORNA
     --------
         Devuelve un condicional if con un mensaje de generación del atchivo pdf.
    '''
    instancia = PersonaAcreditada(cedula,fecha,hora,online=False)
    if (instancia.evaluar()):
        messagebox.showinfo("Información","PDF generado con exito")
        pdf.output('hoja.pdf')

def iniciarsecion ():
    '''
    Funcion que retorna la instancia de la clase App
    Que con tiene la interfaz gráfica del inicio de 
    secion.
    '''
    instacia1=App()
    return instacia1


def solicitarTurno():
    '''
    Función que contiene los parametros Entry y Label de la interfaz
    grafica, además de incluir algunos botones para la validación.

     RETORNO
         No retorna nada.
    '''
    turno=Tk()
    turno.title("Acreditate")
    turno.geometry("800x400")
    turno.config(bg = "gray97")
    
    #agrandar la ventana, abajo arriba, izquierda derecha

    usuario=Frame(turno, width= "1000", height= "1000")
    usuario.config(bg = "gray97")
    usuario.pack()

    #Mensaje de entrada
    mensaje=Label(usuario,text="Acreditate")
    mensaje.grid(row=0, column=1, padx=10, pady=10) 
    mensaje.config(bg="gray97", fg="black", font = ("Arial",16))
    mensaje.focus()
    mensaje1=Label(usuario,text="**Opciones**")
    mensaje1.grid(row=1, column=1, padx=10, pady=10)
    mensaje1.config(bg="gray97", fg="black", font = ("Arial",11))
    mensaje1.focus()
    
    cuadroC=Entry(usuario)
    cuadroC.grid(row=2, column=3, padx=10, pady=10)
    cuadroC.config(justify="center",font = ("Arial",10), bg="gray80",fg="gray1", width=25)
    cuadroC.focus()

    cuadroF=Entry(usuario)
    cuadroF.grid(row=3, column=3, padx=10, pady=10)
    cuadroF.config(justify="center",font = ("Arial",10), bg="gray80",fg="gray1",width=25)
    cuadroF.focus()

    cuadroH=Entry(usuario)
    cuadroH.grid(row=4, column=3, padx=10, pady=10)
    cuadroH.config(justify="center",font = ("Arial",10), bg="gray80",fg="gray1",width=25)
    cuadroH.focus()
    
    #--------------------------------------nombre de cuadros--------------------------------------------------

    fecha=Label(usuario,text="Fecha de entrega (AAAA/MM/DD)")
    fecha.grid(row=3, column=0, padx=10, pady=10)
    fecha.config(justify="left",font = ("Arial",10), bg="gray97",fg="black")
    fecha.focus()
    comprobarF=tk.Button(usuario, text='Comprobar',bg = "gray80", fg="black", font = ("Arial",11),command= lambda: fechavalidada(cuadroF.get()))
    comprobarF.place(x=250, y=140)

    cedula=Label(usuario,text="Digite su cédula")
    cedula.grid(row=2, column=0, padx=10, pady=10)
    cedula.config(justify="left",font = ("Arial",10), bg="gray97",fg="black",)
    cedula.focus()
    comprobarC=tk.Button(usuario, text='Comprobar',bg = "gray80", fg="black", font = ("Arial",11),command= lambda: validadCedula(cuadroC.get()))
    comprobarC.place(x=250, y=100)
    
    hora=Label(usuario,text="Hora de entraga (HH:MM)")
    hora.grid(row=4, column=0, padx=10, pady=10)
    hora.config(justify="left",font = ("Arial",10), bg="gray97",fg="black")
    hora.focus()
    comprobarH=tk.Button(usuario, text='Comprobar',bg = "gray80", fg="black", font = ("Arial",11),command= lambda: validarhora(cuadroH.get()))
    comprobarH.place(x=250, y=180)

    # Botton: genera pdf.
    documento=tk.Button(usuario, text='Evaluar',bg = "gray80", fg="black",font = ("Arial",11), command=lambda:generarPDF(cuadroC.get(),cuadroF.get(),cuadroH.get()))
    documento.grid(row=5, column=2)

def ventanaPrincipal ():
    '''
    Función que contiene los parámetros de la ventana principal
    de la interfaz grádica, ademas de incluir los botones del menú 
    de opciones que permitirá navegar por todo el programa.
    '''
    campos=Tk()
    campos.title("Acreditate")
    campos.geometry("800x400")
    campos.config(bg = "gray97")
    
    #agrandar la ventana, abajo arriba, izquierda derecha
    usuario=Frame(campos, width= "1000", height= "1000")
    usuario.config(bg = "gray97")
    usuario.pack()

    #Mensaje de entrada
    mensaje=Label(usuario,text="Acreditate")
    mensaje.grid(row=0, column=1, padx=10, pady=10) 
    mensaje.config(bg="gray97", fg="black", font = ("Arial",16))
    mensaje.focus()
    mensaje1=Label(usuario,text="**Opciones**")
    mensaje1.grid(row=1, column=1, padx=10, pady=10)
    mensaje1.config(bg="gray97", fg="#4779b2", font = ("Arial",11))
    mensaje1.focus()

    #------------------------------Botones----------------------------
    Button(usuario, text='Apartar turno',command=solicitarTurno,bg = "#4779b2", fg="white", font = ("Arial",11)).grid(row=2, columnspan=3, padx=10, pady=10)
    Button(usuario, text='Registrar Usuario',command= iniciarsecion, bg = "#4779b2", fg="white", font = ("Arial",11)).grid(row=3, columnspan=3, padx=10, pady=10)
    campos.mainloop()




#-------------------------------------------------------- MAIN PRINCIPAL --------------------------------------------#

if __name__ == '__main__':
    '''Conexión con la base de datos mongoDB atraves del puerto 27017'''
    MONGO_HOST="localhost"
    MONGO_PUERTO="27017"
    MONGO_TIEMPO_FUERA=500

    MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO
    '''Llamando a la base de datos y coleccion'''
    MONGO_BASEDATOS="Ciudadanos"
    MONGO_COLECCION="Beneficiarios"

    usuario=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    baseDatos=usuario[MONGO_BASEDATOS]
    mycoleccion=baseDatos[MONGO_COLECCION]
    '''Llamando a la ventana principal de la interfaz gráfica.'''
    ventanaPrincipal()

    #2300521914

