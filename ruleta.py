import random

def ruleta_rusa():
    print("girando cargadores...")
    while True:    
        try:
            cargador=[1,2,3,4,5,6]
            bala=int(input("bala numero...: "))
            ruleta=random.choice(cargador)
            if bala<1:
                print("solo tienes 6 posibilidades, elige entre 1 y 6...")
                continue
            if bala>6:
                print("solo tienes 6 posibilidades, elige entre 1 y 6...")
                continue
            if ruleta == bala:
                print("PERDISTE")
                break
            else:
                print("SIGUES VIVO, DE MOMENTO...")
        except ValueError:
            print("por favor introduce un numero...")

ruleta_rusa()

