import time
from termcolor import colored

def sleep(t):
    return time.sleep(t)

def menu():
    print("---------------------------------------------------------")
    name = input("Quel est votre nom ?")
    print("Bonjour", name, "!")
    sleep(0)
    print("Ce programme génère aléatoirement les questions et réponses du QCM que vous avez choisi !")
    sleep(0)
    print("Vous êtes pret ? y/n")
    print("---------------------------------------------------------")
    ready = ""
    while ready.lower() != "y":
        ready = input("==> ") 
        if ready == "y":
            sleep(0)
        else:
            print("Ok, prends ton temps../") 
            sleep(0)
            print("Et maintenant ?")   
    cotation_presentation()   

def cotation_presentation():
    print("Il y a 3 systèmes de cotation, le classique = 1, celui à point négatif = 2, \net le dernier qui est un système de cotation pondéré !\n ")

def color(text, color):
    return print(colored(text, color, attrs=['bold', 'blink', "reverse"]))
