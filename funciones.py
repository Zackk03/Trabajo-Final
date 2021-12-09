import os, webbrowser, Registro_ANIME, folium, geopy, time
from sqlite3.dbapi2 import OptimizedUnicode, connect, register_adapter
import sqlite3 as sql
from prettytable import from_db_cursor
from geopy import Nominatim
from tqdm import tqdm

#MENUS Y DISTINTOS BANNERS---------------------------

confirmacion = """
----[Confirmación]-----------------------------------+
                                                     |
    [1] - Comenzar                                   |
    [2] - Regresar                                   |
                                                     |
-----------------------------------------------------+
"""
confirmacion_ter = """
----[¿Seguro que desea continuar?]-------------------+
                                                     |
    [1] - Terminar                                   |
    [2] - Cancelar                                   |
                                                     |
-----------------------------------------------------+
"""
sexo = """
----[Elija el sexo del personaje]--------------------+
                                                     |
    [1] - Masculino                                  |
    [2] - Femenino                                   |
    [3] - Otro                                       |
                                                     |
-----------------------------------------------------+
"""
opt_estado = """
----[Elija el estado del personaje]------------------+
                                                     |
    [1] - Vivo                                       |
    [2] - Muerto                                     |
    [3] - Indefinido                                 |
                                                     |
-----------------------------------------------------+
"""
gestionar = """
----[Elija una opción]-------------------------------+
                                                     |
    [1] - Agregar Personaje                          |
    [2] - Modificar Personaje                        |
    [3] - Eliminar Personaje                         |
    [4] - Regresar                                   |
                                                     |
-----------------------------------------------------+
"""
error = """

███████╗██████╗ ██████╗  ██████╗ ██████╗ 
██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗
███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
Lo que está seleccionando no existe\nPor favor intente con un dato registrado.    

"""
configuracion = """
----[Configuración]-----------------------------------+
                                                      |
    [1] - Series                                      |
    [2] - Estados                                     |
    [3] - Sexo                                        |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
series = """
----[Series]------------------------------------------+
                                                      |
    [1] - Agregar Serie                               |
    [2] - Editar Serie                                |
    [3] - Eliminar Serie                              |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
estados = """
----[Estados]-----------------------------------------+
                                                      |
    [1] - Agregar Estado                              |
    [2] - Editar Estado                               |
    [3] - Eliminar Estado                             |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
generos = """
----[Género]------------------------------------------+
                                                      |
    [1] - Agregar Género                              |
    [2] - Editar Género                               |
    [3] - Eliminar Género                             |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
actualizar = """"
----[¿Qué desea actualizar?]--------------------------+
                                                      |
    [1]  - Nombre                                     |
    [2]  - Apellido                                   |
    [3]  - Foto                                       |
    [4]  - Pronunciación                              |
    [5]  - Serie                                      |
    [6]  - Fecha de Nacimiento                        |
    [7]  - Poder                                      |
    [8]  - Frase Favorita                             |
    [9]  - Vestimenta del Personaje                   |
    [10]  - Edad                                      |
    [11] - Altura                                     |
    [12] - Sexo                                       |
    [13] - Estado                                     |
    [14] - Dirección                                  |
    [15] - Regresar                                   |
                                                      |
------------------------------------------------------+
"""
reportar = """
----[Cómo deseas generar un reporte]------------------+
                                                      |
    [1] - Listado de Personajes                       |
    [2] - Listado de Personajes por Signo Zodiacal    |
    [3] - Mapa con Todos lo Personajes                |
    [4] - Exportar Personajes a HTML                  |
    [5] - Listado de Personajes por Serie             |
    [6] - Listado de Personajes por Estado            |
    [7] - Regresar                                    |
                                                      |
------------------------------------------------------+
""" 
Signos = """
---[Signos del Zodiaco]-------------------------------+
                                                      |
    ¿Por cual Signo del Zodiaco, desea filtrar        |
    a los personajes?                                 |
                                                      |
        [1]  - Aries                                  |
        [2]  - Tauro                                  |
        [3]  - Géminis                                |
        [4]  - Cáncer                                 |
        [5]  - Leo                                    |
        [6]  - Virgo                                  |
        [7]  - Libra                                  |
        [8]  - Escorpión                              |
        [9]  - Sagitario                              |
        [10] - Capricornio                            |
        [11] - Acuario                                |
        [12] - Piscis                                 |
        [13] - Cancelar                               |
                                                      |
------------------------------------------------------+
"""
config = """
----[¿Qué desea configurar?]--------------------------+
                                                      |
    [1] - Series                                      |
    [2] - Estados                                     |
    [3] - Sexos                                       |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
config_serie = """
----[¿Qué desea configurar?]--------------------------+
                                                      |
    [1] - Agregar Serie                               |
    [2] - Modificar Serie                             |
    [3] - Eliminar Serie                              |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
config_estado = """
----[¿Qué desea configurar?]--------------------------+
                                                      |
    [1] - Agregar Estado                              | 
    [2] - Modificar Estado                            |
    [3] - Eliminar Estado                             |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""
config_sexo = """
----[¿Qué desea configurar?]--------------------------+
                                                      |
    [1] - Agregar Sexo                                |
    [2] - Modificar Sexo                              |
    [3] - Eliminar Sexo                               |
    [4] - Regresar                                    |
                                                      |
------------------------------------------------------+
"""


#CREACION DE LA DB-----------------------------------#
def createdb():
    conn = sql.connect("Registro_ANIME.db")
    conn.commit()
    conn.close()

#CREACION DE TABLAS--------------------------------------#
def createtable():
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE Registro_ANIME(
        Nombre varchar(50),
        Apellido varchar(50),
        Foto varchar(100),
        Pronunciacion varchar(50),
        Serie varchar(50),
        Fecha de Nacimiento varchar(50),
        Poder varchar(50),
        Frase Favorita varchar(100),
        Vestimenta varchar(100),
        Edad varchar(50),
        Altura varchar(50),
        Sexo varchar(50),
        Estado varchar(50),
        Signo Zodical varchar(50),
        Direccion varchar(50),
        Latitud real,
        Longitud real)
        """)
    conn.commit()
    conn.close()

#CREACION DE LA DB (SERIES)--------------------------#
def createdb_s():
    conn = sql.connect("Registro_SERIES.db")
    conn.commit()
    conn.close()

def createtable_s():
    conn = sql.connect("Registro_SERIES.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE Registro_SERIES(
        Series varchar(50) PRIMARY KEY
    )
    """)
    conn.commit()
    conn.close()

#CREACION DE LA DB (SEXO)----------------------------#
def createdb_sx():
    conn = sql.connect("Registro_SEXO.db")
    conn.commit()
    conn.close()

def createtable_sx():
    conn = sql.connect("Registro_SEXO.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE Registro_SEXO(
        Generos varchar(50) PRIMARY KEY
    )
    """)
    conn.commit()
    conn.close()

#CREACION DE LA DB (ESTADO)--------------------------#
def createdb_est():
    conn = sql.connect("Registro_ESTADO.db")
    conn.commit()
    conn.close()

def createtable_est():
    conn = sql.connect("Registro_ESTADO.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE Registro_ESTADO(
        Estados varchar(50) PRIMARY KEY
    )
    """)
    conn.commit()
    conn.close()

#GESTIONAR-----------------------------------------------#
def gestionar_p():
    try:
        os.system("cls")
        print(gestionar)
        opcion = int(input("Ingrese una opción >> "))
        if opcion == 1:
            createrow()

        elif opcion == 2:
            os.system("cls")
            print(actualizar)
            opcion = int(input("Ingrese la opción deseada >> "))
            if opcion == 1:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_nombre = input("Ingrese el nuevo nombre del personaje: ")
                update_p("ANIME", "Nombre", "Nombre", nombre, n_nombre)
            
            elif opcion == 2:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_ape = input("Ingrese el nuevo apellido del personaje: ")
                update_p("ANIME", "Apellido", "Nombre", nombre, n_ape)

            elif opcion == 3:
                os.system("cls")
                showtable()
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_foto = input("Ingrese la nueva URL de la foto nombre del personaje: ")
                update_p("ANIME", "Foto", "Nombre", nombre, n_foto)

            elif opcion == 4:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_pronu = input("Ingrese la nueva pronunciación del personaje: ")
                update_p("ANIME", "Pronunciacion", "Nombre", nombre, n_pronu)
                
            elif opcion == 5:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_serie = input("Ingrese el nuevo nombre de la serie, donde aparece el  personaje: ")
                update_p("ANIME", "Serie", "Nombre", nombre, n_serie)

            elif opcion == 6:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_fecha = input("Ingrese la nueva fecha de nacimiento del personaje: ")
                update_p("ANIME", "Fecha de Nacimiento", "Nombre", nombre, n_fecha)

            elif opcion == 7:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_poder = input("Ingrese el nuevo poder del personaje: ")
                update_p("ANIME", "Poder", "Nombre", nombre, n_poder)

            elif opcion == 8:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_frase = input("Ingrese la nueva frase favorita del personaje: ")
                update_p("ANIME", "Frase Favorita", "Nombre", nombre, n_frase)
            
            elif opcion == 9:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_vesti = input("Ingrese la nueva descripción de la vestimenta del personaje: ")
                update_p("ANIME", "Vestimenta", "Nombre", nombre, n_vesti)
            
            elif opcion == 10:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_edad = input("Ingrese la nueva edad del personaje: ")
                update_p("ANIME", "Edad", "Nombre", nombre, n_edad)
            
            elif opcion == 11:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_altura = input("Ingrese la nueva altura del personaje: ")
                update_p("ANIME", "Altura", "Nombre", nombre, n_altura)
            
            elif opcion == 12:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_sexo = input("Ingrese el nuevo género del personaje: ")
                update_p("ANIME", "Sexo", "Nombre", nombre, n_sexo)
            
            elif opcion == 13:
                os.system("cls")
                showtable()
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_estado = input("Ingrese el nuevo estado del personaje: ")
                update_p("ANIME", "Estado", "Nombre", nombre, n_estado)
            
            elif opcion == 14:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje a modificar: ")
                n_direccion = input("Ingrese la nueva dirección del personaje: ")
                update_p("ANIME", "Direccion", "Nombre" ,  nombre, n_direccion)
            
            elif opcion == 15:
                Registro_ANIME.main()
                
        elif opcion == 3:
            os.system("cls")
            showtable("ANIME")
            nombre = input("Ingrese el nombre del personaje eliminar: ")
            eliminar("ANIME", nombre, "Nombre")
        elif opcion == 4:
            Registro_ANIME.main()
        elif opcion != 1 or opcion != 2 or opcion != 3:
            input("Ingrese la opción correspondiente")
            gestionar_p()
    except:
        input("Ingrese la opción correspondiente")
        gestionar_p()


#INTRODUCCION DE DATOS A LAS DB---------------------------#
def createrow():
    try:
        os.system("cls")
        print(confirmacion)
        opcion = int(input("Ingrese la opción deseada >> "))
        if opcion == 2:
            gestionar_p()
        else:
            if opcion == 1:
                os.system("cls")
                showtable("ANIME")
                nombre = input("Ingrese el nombre del personaje: ")
                apellido = input("Ingrese el apellido del personaje: ")
                foto = input("Ingrese la URL de la foto del personaje: ")
                pronunciacion = input("Ingrese la pronunciación del nombre del personaje: ")
                serie = input("Ingrese la serie en donde sale el personaje: ")
                fecha_naci = input("Ingrese la fecha de nacimiento del personaje dd/mm/yyyy: ")
                poder = input("Ingrese el poder del personaje: ")
                frase = input("Ingrese la frase favorita del personaje: ")
                vestimenta = input("Ingrese una breve descripción de la vestimenta del personaje: ")
                edad = input("Ingrese la edad del personaje: ")
                altura = input("Ingrese la altura del personaje: ")
                
                #SEXO DEL PERSONAJE------------------------------------------#
                try:
                    os.system("cls")
                    print(sexo)
                    opt_sexo = int(input("Ingrese la opción deseada >> "))
                    if opt_sexo == 1:
                        genero = "Masculino"
                    elif opt_sexo == 2:
                        genero = "Femenino"
                    elif opt_sexo == 3:
                        genero = input("Ingrese el sexo del personaje: ")
                except:
                    input("ingrese una opción válida")

                #ESTADO DEL PERSONAJE-----------------------------------------#
                try:
                    os.system("cls")
                    print(opt_estado)
                    opt_est = int(input("Ingrese la opción deseada >> "))
                    if opt_est == 1:
                        estado = "Vivo"
                    elif opt_est == 2:
                        estado = "Muerto"
                    elif opt_est == 3:
                        estado = "Indefinido"
                except:
                    input("ingrese una opción válida")

                os.system("cls")
                direccion = input("Ingrese la dirección de dónde vive el personaje: ")
                
                #LATITUD Y LONGITUD----------------------------------------------#
                try:
                    geo = Nominatim(user_agent="Latitudelng")
                    loc = geo.geocode(f"{direccion}")
                    latitud = loc.latitude
                    longitud = loc.longitude
                except:
                    latitud = 18.1213547
                    longitud = -71.4874852
                
                #SIGNO ZODIACAL-----------------------------------------------------#
                dia = int(fecha_naci[0:2])
                mes = int(fecha_naci[3:5])
                if (dia >= 21 and mes == 3) or (dia <= 20 and mes == 4):
                    signo = ("Aries")
                elif (dia >= 21 and mes == 4) or (dia <= 21 and mes == 5):
                    signo = ("Tauro")
                elif (dia >= 22 and mes == 5) or (dia <= 21 and mes == 6):
                    signo = ("Géminis")
                elif (dia >= 22 and mes == 6) or (dia <= 22 and mes == 7):
                    signo = ("Cáncer")
                elif (dia >= 23 and mes == 7) or (dia <= 23 and mes == 8):
                    signo = ("Leo")
                elif (dia >= 24 and mes == 8) or (dia <= 23 and mes == 9):
                    signo = ("Virgo")
                elif (dia >= 23 and mes == 9) or (dia <= 22 and mes == 10):
                    signo = ("Libra")
                elif (dia >= 24 and mes == 10) or (dia <= 22 and mes == 11):
                    signo = ("Escorpión")
                elif (dia >= 23 and mes == 11) or (dia <= 21 and mes == 12):
                    signo = ("Sagitario")
                elif (dia >= 22 and mes == 12) or (dia <= 20 and mes == 1):
                    signo = ("Capricornio")
                elif (dia >= 21 and mes == 1) or (dia <= 18 and mes == 2):
                    signo = ("Acuario")
                elif (dia >= 19 and mes == 2) or (dia <= 20 and mes == 3):
                    signo = ("piscis")


                conn = sql.connect("Registro_ANIME.db")
                cursor = conn.cursor()
                instruccion = f"INSERT INTO Registro_ANIME VALUES ('{nombre}','{apellido}','{foto}','{pronunciacion}','{serie}','{fecha_naci}','{poder}','{frase}','{vestimenta}',{edad},'{altura}','{genero}','{estado}','{signo}','{direccion}',{latitud},{longitud})"
                conexion_serie(serie)
                conexion_sexo(genero)
                conexion_estado(estado)
                cursor.execute(instruccion)
                conn.commit()
                conn.close()
                Registro_ANIME.main()
    except:
        input("Ingrese datos válidos por favor")
        Registro_ANIME.main()

def conexion_serie(serie):
    try:
        conn = sql.connect("Registro_SERIES.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Registro_SERIES VALUES ('{serie}')")
        conn.commit()
        conn.close()
    except:
        conn.close()

def conexion_sexo(genero):
    try:
        conn = sql.connect("Registro_SEXO.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Registro_SEXO VALUES ('{genero}')")
        conn.commit()
        conn.close()
    except:
        conn.close()

def conexion_estado(estado):
    try:
        conn = sql.connect("Registro_ESTADO.db")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Registro_ESTADO VALUES ('{estado}')")
        conn.commit()
        conn.close()
    except:
        conn.close()

def createrow_extra(db, mensaje):
    try:
        os.system("cls")
        print(confirmacion)
        opcion = int(input("Ingrese la opción deseada >> "))
        if opcion == 2:
            settings()
        else:
            if opcion == 1:
                os.system("cls")
                showtable(f"{db}")
                nombre = input(f"{mensaje}")
                conn = sql.connect(f"Registro_{db}.db")
                cursor = conn.cursor()
                instruccion = f"INSERT INTO Registro_{db} VALUES ('{nombre}')"
                cursor.execute(instruccion)
                conn.commit()
                conn.close()
                Registro_ANIME.main()
    except:
        input("Ingrese los datos correctos...")
        Registro_ANIME.main()


#ELIMINAR PERSONAJE------------------------------------------#
def eliminar(db, nombre, parametro):
    try:
        os.system("cls")
        conn = sql.connect(f"Registro_{db}.db")
        cursor = conn.cursor()
        Registro_anime = cursor.fetchall()
        len(Registro_anime)
        instruccion = f"DELETE FROM Registro_{db} WHERE {parametro}='{nombre}'"
        os.system("cls")
        print(confirmacion_ter)
        opcion = int(input("Ingrese la opción deseada >> "))
        if opcion == 2:
            gestionar_p()
        elif opcion == 1:
            cursor.execute(instruccion)
            conn.commit()
            conn.close()
            Registro_ANIME.main()
    except:
        input("Ingrese una opción válida")
        Registro_ANIME.main()

#MODIFICAR PERSONAJE---------------------------------------#
def update_p(db, parametro, doparametro, nombre, n_valor):
    try:
        os.system("cls")
        conn = sql.connect(f"Registro_{db}.db")
        cursor = conn.cursor()
        instruccion = f"UPDATE Registro_{db} SET {parametro}='{n_valor}' WHERE {doparametro}='{nombre}'"
        cursor.execute(instruccion)
        conn.commit()
        conn.close()
        Registro_ANIME.main()
    except:
        input("Personaje incorrecto, Ingrese el nombre del personaje de forma correcta...")
        Registro_ANIME.main()

#MOSTRAR TABLA---------------------------------------------#
def showtable(nombre):
    conn = sql.connect(f"Registro_{nombre}.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Registro_{nombre}")
    x = from_db_cursor(cursor)
    print(x)

#LISTADO DE PERSONAJES-------------------------------------#
def list_p():
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    instruccion = "SELECT Nombre, Apellido, Serie, Sexo, Edad FROM Registro_ANIME"
    cursor.execute(instruccion)
    x = from_db_cursor(cursor)
    print(x)

def list_p_serie():
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    instruccion = "SELECT Nombre, Serie FROM Registro_ANIME"
    cursor.execute(instruccion)
    x = from_db_cursor(cursor)
    print(x)

def list_p_est():
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    instruccion = "SELECT Nombre, Estado FROM Registro_ANIME"
    cursor.execute(instruccion)
    x = from_db_cursor(cursor)
    print(x)

#SIGNO ZODIACAL---------------------------------------------#
def signoz(signo):
    os.system("cls")
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    instruccion = f"SELECT Nombre, Signo FROM Registro_ANIME WHERE Signo='{signo}'"
    cursor.execute(instruccion)
    x = from_db_cursor(cursor)
    print(f"Estos son todos los personajes con signo {signo}.")
    print(x)
    input("Presione Enter para continuar...")
    Registro_ANIME.main()
    
def signozodical():
    os.system("cls")
    print(Signos)
    opcion = int(input("Ingrese la opción deseada >> "))
    if opcion == 1:
        signoz("Aries")
    elif opcion == 2:
        signoz("Tauro")
    elif opcion == 3:
        signoz("Geminis")
    elif opcion == 4:
        signoz("Cancer")
    elif opcion == 5:
        signoz("Leo")
    elif opcion == 6:
        signoz("Virgo")
    elif opcion == 7:
        signoz("Libra")
    elif opcion == 8:
        signoz("Escorpion")
    elif opcion == 9:
        signoz("Sagitario")
    elif opcion == 10:
        signoz("Capricornio")
    elif opcion == 11:
        signoz("Acuario")
    elif opcion == 12:
        signoz("Piscis")
    elif opcion == 13:
        Registro_ANIME.main()

#ACERCA DE (VIDEO EXPLICATIVO)-------------------------------#
def about():
    webbrowser.open_new_tab("https://www.youtube.com/watch?v=PW8hJRyP0b0")
    Registro_ANIME.main()

#MAPA CON LOS DATOS-----------------------------------------#
def mapa():
    os.system("cls")
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    instruccion = "SELECT * FROM Registro_ANIME"
    cursor.execute(instruccion)
    Registro_anime = cursor.fetchall()
    m = folium.Map(location=[17.6500232, -8.1247721], zoom_start=5, tiles="Stamen Terrain")
    for i in range(len(Registro_anime)):
        nombre = Registro_anime[i][0]
        apellido = Registro_anime[i][1]
        serie = Registro_anime[i][4]
        Latitud = Registro_anime[i][15]
        Longitud = Registro_anime[i][16]
        marker = folium.Marker(location=[Latitud, Longitud], popup=f"<i>{nombre} {apellido}, {serie}</i>", icon=folium.Icon(color="red"))
        marker.add_to(m)
    m.save("mapa.html")
    loading()
    webbrowser.open_new_tab("mapa.html")
    Registro_ANIME.main()

#HTML-------------------------------------------------------#
def html(personaje):
    os.system("cls")
    conn = sql.connect("Registro_ANIME.db")
    cursor = conn.cursor()
    instruccion =f"SELECT * FROM Registro_ANIME WHERE Nombre='{personaje}'"
    cursor.execute(instruccion)
    Registro_anime = cursor.fetchall()
    contador = cursor.execute(instruccion).rowcount
    if contador == 0:
        os.system("cls")
        print(error)
        time.sleep(5)
        reportes() 
    for i in range(len(Registro_anime)):
        nombre = Registro_anime[i][0]
        apellido = Registro_anime[i][1]
        foto = Registro_anime[i][2]
        pronunciacion = Registro_anime[i][3]
        serie = Registro_anime[i][4]
        fecha = Registro_anime[i][5]
        poder = Registro_anime[i][6]
        frase = Registro_anime[i][7]
        vesti = Registro_anime[i][8]
        edad = Registro_anime[i][9]
        altura = Registro_anime[i][10]
        sexo = Registro_anime[i][11]
        estado = Registro_anime[i][12]
        signo = Registro_anime[i][13]
        direccion = Registro_anime[i][14]
    html = f"""
<link rel="stylesheet" href="estilos.css">
<table>
    <caption><marquee>Datos del usuario</marquee></caption>
    <thead>
        <th>Foto</th>
        <th>Nombre</th>
        <th>Apellido</th>
        <th>Pronunciacion</th>
        <th>Serie</th>
        <th>Fecha</th>
        <th>Poder</th>
        <th>Frase</th>
        <th>Vestimenta</th>
        <th>Edad</th>
        <th>Altura</th>
        <th>Genero</th>
        <th>Estado</th>
        <th>Signo</th>
        <th>Direccion</th>
    </thead>
    <tbody>
        <td><img src="{foto}" alt=""></td>
        <td>{nombre}</td>
        <td>{apellido}</td>
        <td>{pronunciacion}</td>
        <td>{serie}</td>
        <td>{fecha}</td>
        <td>{poder}</td>
        <td>{frase}</td>
        <td>{vesti}</td>
        <td>{edad}</td>
        <td>{altura}</td>
        <td>{sexo}</td>
        <td>{estado}</td>
        <td>{signo}</td>
        <td>{direccion}</td>
    </tbody>
</table>
"""
    nombre_archivo = "Datos.html"
    archivo = open(nombre_archivo, "w")
    archivo.write(html)
    archivo.close()
    loading()
    webbrowser.open_new_tab(nombre_archivo)
    Registro_ANIME.main()

#LOADING BAR-----------------------------------------------#
def loading():
    loop = tqdm(total=2000, position=0, leave=False)
    for k in range(2000):
        loop.set_description("loading...".format(k))
        loop.update(1)
    loop.close()

#EXPORTAR--------------------------------------------------#
def reportes():
    try:
        os.system("cls")
        print(reportar)
        opcion = int(input("Ingrese la opción deseada >> "))
        if opcion == 1:
            os.system("cls")
            print("Listado de Personajes")
            list_p()
            input("Pulse Enter para regresar...")
            Registro_ANIME.main()

        elif opcion == 2:
            signozodical()
        elif opcion == 3:
            mapa()
        elif opcion == 4:
            os.system("cls")
            showtable("ANIME")
            opcion = input("Ingrese el personaje a exportar: ")
            html(opcion)
        elif opcion == 5:
            os.system("cls")
            print("Listado de personajes por Serie")
            list_p_serie()
            input("Pulse Enter para regresar...")
            Registro_ANIME.main()
        elif opcion == 6:
            os.system("cls")
            print("Listado de personajes por su estado")
            list_p_est()
            input("Pulse Enter para regresar...")
            Registro_ANIME.main()
        elif opcion == 7:
            Registro_ANIME.main()
        elif opcion != 1 or opcion != 2 or opcion != 3 or opcion != 4 or opcion != 5 or opcion != 6 or opcion != 7:
            input("Ingrese una opción válida por favor")
            reportes()
    except:
        input("Ingrese una opción válida por favor")
        reportes()

#CONFIGURACION--------------------------------------------#
def settings():
    try:
        os.system("cls")
        print(config)
        opcion = int(input("Ingrese la opción deseada >> "))
        if opcion == 1:
            os.system("cls")
            print(config_serie)
            opcion = int(input("Ingrese la opción deseada >> "))
            if opcion == 1:
                createrow_extra("SERIES", "Ingrese el nombre de la serie: ")
            elif opcion == 2:
                os.system("cls")
                showtable("SERIES")
                nombre = input("Ingrese el nombre de la serie a modificar: ")
                n_nombre = input("Ingrese el nuevo nombre de la serie: ")
                update_p("SERIES", "Series", "Series", nombre, n_nombre)
            elif opcion == 3:
                os.system("cls")
                print(confirmacion)
                opt = int(input("Ingrese la opción deseada >> "))
                if opt == 1:
                    os.system("cls")
                    showtable("SERIES")
                    nombre = input("Ingrese el nombre de la serie que desea eliminar o bien pulse 's' para salir: ")
                    if nombre == "s":
                        settings()
                    else:
                        eliminar("SERIES", nombre, "Series")
                elif opt == 2:
                    settings()
            elif opcion == 4:
                Registro_ANIME.main()

        elif opcion == 2:
            os.system("cls")
            print(config_estado)
            opcion = int(input("Ingrese la opción deseada >> "))
            if opcion == 1:
                createrow_extra("ESTADO", "Ingrese el estado: ")
            elif opcion == 2:
                os.system("cls")
                showtable("ESTADO")
                estado = input("Ingrese el estado a modificar: ")
                n_estado = input("Ingrese el nuevo estado: ")
                update_p("ESTADO", "Estados", "Estados", estado, n_estado)
            elif opcion == 3:
                os.system("cls")
                print(confirmacion)
                opt = int(input("Ingrese la opción deseada >> "))
                if opt == 1:
                    os.system("cls")
                    showtable("ESTADO")
                    nombre = input("Ingrese el estado que desea eliminar o bien pulse 's' para salir: ")
                    if nombre == "s":
                        settings()
                    else:
                        eliminar("ESTADO", nombre, "Estados")
                elif opt == 2:
                    settings()
            elif opcion == 4:
                Registro_ANIME.main()

        elif opcion == 3:
            os.system("cls")
            print(config_sexo)
            opcion = int(input("Ingrese la opción deseada >> "))
            if opcion == 1:
                createrow_extra("SEXO", "Ingrese el género: ")
            elif opcion == 2:
                os.system("cls")
                showtable("SEXO")
                genero = input("Ingrese el género a modificar: ")
                n_genero = input("Ingrese el nuevo género: ")
                update_p("SEXO", "Generos", "Generos", genero, n_genero)
            elif opcion == 3:
                os.system("cls")
                print(confirmacion)
                opt = int(input("Ingrese la opción deseada >> "))
                if opt == 1:
                    os.system("cls")
                    showtable("SEXO")
                    nombre = input("Ingrese el género que desea eliminar o bien pulse 's' para salir: ")
                    if nombre == "s":
                        settings()
                    else:
                        eliminar("SEXO", nombre, "Generos")
                elif opt == 2:
                    settings()
            elif opcion == 4:
                Registro_ANIME.main()
        elif opcion == 4:
            os.system("cls")
            Registro_ANIME.main()   
    except:
        input("Ingrese la opción una opción válida")
        Registro_ANIME.main()

#GOOGLE SITE-----------------------------------------------#
def googlesite():
    webbrowser.open_new_tab("https://sites.google.com/view/erickgm20210821/inicio")
    Registro_ANIME.main()     

#MENCION DE FUNCION PRINCIPAL-----------------------------#
if __name__=="__main__":
    #createdb()
    #createtable()
    #createdb_s()
    #createdb_est()
    #createdb_sx()
    #createtable_s()
    #createtable_sx()
    #createtable_est()
    #createdbsz()
    #createtablesz()
    #signoz()
    #createrow()
    #loading_main()
    reportes()