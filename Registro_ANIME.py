import funciones, os

menu = """
----[Registro de ANIMES]-----------------------------------+
                                                           |
    [1] - Gestionar Personajes                             |
    [2] - Reportes                                         |
    [3] - Configuración                                    |
    [4] - Acerca De                                        |
    [5] - Sitio Web                                        |
    [6] - Salir                                            |                                                            
                                By: Erick García Méndez    |
-----------------------------------------------------------+   
"""

#FUNCION PRINCIPAL-----------------------------------------#
def main():
    try:
        os.system("cls")
        print(menu)
        opcion = int(input("Ingrese la opción deseada >> "))
        if opcion == 1:
            os.system("cls")
            funciones.gestionar_p()
        elif opcion == 2:
            os.system("cls")
            funciones.reportes()
        elif opcion == 3:
            os.system("cls")
            funciones.settings()
        elif opcion == 4:
            os.system("cls")
            funciones.about()
        elif opcion == 5:
            os.system("cls")
            funciones.googlesite()
        elif opcion == 6:
            opcion = input("¿Desea Salir? [s/n] >> ")
            if opcion == "s":
                os.system("exit")
            elif opcion == "n":
                main()
            else:
                input("Ingrese una opción válida 's' para aceptar o 'n' para cancelar...")
                main()
        elif opcion != 1 or opcion != 2 or opcion != 3 or opcion != 4 or opcion != 5 or opcion != 6:
            input("Ingrese la opción correspondiente")
            main()
    except:
        input("Ingrese la opción correspondiente")
        main()

#MENCION DE FUNCION PRINCIPAL-----------------------------#
if __name__=="__main__":
    main()
