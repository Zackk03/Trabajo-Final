import os
#Add two numbers----------------------------------#
try:
    addanother = True
    while addanother:
        os.system("cls")
        fnum = int(input("Add the first number: ")) 
        snum = int(input("Add the second number: "))
        result = fnum + snum
        print("The result is: " + str(result))

        option = input("Would you add another two numbers? [y/n] >> ")
        if option == "y":
            addanother = True
        elif option == "n":
            break
except:
    input("Add a correct values!")
