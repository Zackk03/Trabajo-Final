import os
#Sumar dos números----------------------------------#
try:
    continuacion = True
    while continuacion:
        os.system("cls")
        pnum = int(input("Ingrese el primer número: ")) 
        snum = int(input("Ingrese el segundo número: "))
        resultado = pnum + snum
        print("El resultado es: " + str(resultado))

        opcion = input("¿Desea sumar dos número de nuevo? [s/n] >> ")
        if opcion == "s":
            continuacion = True
        elif opcion == "n":
            break
except:
    input("¡Ingrese datos válidos!")