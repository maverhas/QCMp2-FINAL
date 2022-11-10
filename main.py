
from menu import menu, sleep
from termcolor import colored
import random
import string
import sys
import time
from Correctif import correctif


# ce que j'ai rajouté
def build_questionnaire(filename):
    """
        Construit le QCM avec les questions contenue dans le fichier donné.
        :type filename: Un string représentant le nom du fichier a charger.

        :return: Une liste de questions
    """
    questions = []
    wording = None
    choices = []
    with open(filename, encoding='utf-8') as file:
        for line in file.readlines():
            if '|' not in line:
                if wording or choices:
                    questions.append([wording, choices])
                wording = None
                choices = []
            else:
                parts = line.strip().split('|')
                if 1 < len(parts) < 5:
                    if parts[0] == 'Q':
                        if not wording and not choices:
                            wording = parts[1]
                            choices = []
                        else:
                            questions.append([wording, choices])
                            wording = None
                            choices = []
                    elif parts[0] == 'A':
                        if parts[2] not in ('V', 'X'):
                            print("Error when loading line:\n\t{}".format(line))
                        else:
                            choices.append([parts[1], parts[2] == 'V', parts[3] if len(parts) > 3 else ''])
                    else:
                        print("Error when loading line:\n\t{}".format(line))
                else:
                    print("Error when loading line:\n\t{}".format(line))

                if line.startswith('Q'):
                    wording = parts[1]

    if wording or choices:
        questions.append([wording, choices])
    return questions
    
def cotation1(list_of_answers): 
    #cotation 1 classique : 
    # pré : nombre de réponses vrai 
    # post : renvoie la cotation classique finale
    i = 0
    for answer in list_of_answers:
        if answer == True:
            i+=1
        elif answer == False:
            i+=0
        elif answer == None:
            i+=0
    if i < 0:
        i = 0  
    return i 



def cotation2(list_of_answers): 
    #cotation à point négative : 
    # pré : nombre de réponse vrai (+1) et nombre de réponse fausse (-1)
    # post : renvoie la cotation à point negative finale
    i = 0
    for answer in list_of_answers:
        if answer == True:
            i+=1
        elif answer == False:
            i-=1
        elif answer == None:
            i+=0
    if i < 0:
        i = 0  
    return i


    
def cotation3(list_of_answers, list_pour_lesperance):
    #cotation pondérée : 
    # pré : nombre de réponse vrai (+1) et nombre de réponse fausse (- l'esperence )
    # on calcule l'esperance
    # post : renvoie la cotation à point negative pondéré finale
    i = 0
    k = 0
    for answer in list_of_answers:
        if len(list_pour_lesperance[k]) == 1:
            esperancex = 0
        else:
            esperancex = -(1/(len(list_pour_lesperance[k]) - 1)) 
        if answer == True:
            i+=1
        elif answer == False:
            i = i + esperancex
        elif answer == None:
            i+=0
        k += 1
    if i < 0:
        i = 0    
    return i



def resultat_final(i, questions):
    # resultat final :
    # pré : cotation final 
    # post : renvoie une appréciation selon la cotation
    lenght = len(questions)
    if i < lenght/2:
        print(f"{i}/{lenght}")
        print("C'est pas fameux...")
    elif i == lenght/2:
        print(f"{i}/{lenght}")
        print("Peut mieux faire")
    elif lenght > i > lenght/2:
        print(f"{i}/{lenght}")
        print("Bien !")
    elif i == lenght:
        print(f"{i}/{lenght}")
        print("Parfait !")

def color(text, color):
    return print(colored(text, color, attrs=['bold', 'blink', "reverse"]))


        
def random_QCM(choose_quest):
    # rendre le QCM aléatoire :
    # pré : document txt 
    # post : renvoie les choix aléatoires dans une liste
    questions = build_questionnaire(f"{choose_quest}")
    while True:
        list_random = []
        aleatoire_choice = random.choices(questions, k = len(questions))
        for element in aleatoire_choice:
            if element not in list_random:
                list_random.append(element)
        if len(list_random) == len(aleatoire_choice):
            break
    return list_random

    


def Quizz():
    #Fonction principale du code qui génère le qcm
    #pré : /
    #post : Affiche le jeux qcm dans son intégralité
    run = True
    print("Bienvenue dans le menu de ce générateur de QCM ! Veuillez suivre les instructions qui vont suivre.") #Introductio du qcm
    while run:#Boucle principale qui permet de faire tourner le programme jusqu'a ce que l'utilisateur décide de s'arreter, permet de faire plusieurs parties.
        while True:
            choose_quest = input("Insérez le nom du fichier qui contient vos questions : \n ==>")
            try: #Gestion des erreures, pour s'assurer que l'utilisateur rentre un document existant
                files = open(f"{choose_quest}.txt", "r")
                files.close()
                break
            except:
                print("Ce fichier n'existe pas...")
        menu()
        print("Avec quel systeme de cotation voulez-vous jouer ?")
        while True: #Choix du type de cotation, boucle qui permet de redemander le type de cotation tant que l'utilisateur ne rentre pas un chiffre correct.
            syst_cot = input("==> ")
            if syst_cot == "1":
                a = 0
                break
            elif syst_cot == "2":
                a = 1
                break
            elif syst_cot== "3":
                a = 2
                break
            else:
                print("Cela n'existe pas !")
        sleep(0.5)
        print("Bonne chance !")
        print("---------------------")
        questionnaire = random_QCM(choose_quest + ".txt")#Variable contenant la fonctions qui permet d'afficher les questions aléatoirement.
        
        # ici je stock toutes les questions
        
        number_of_questions = []
        list_pour_lesperance = []
        for i in range(0, len(questionnaire)):
            h = questionnaire[i][0]
            number_of_questions.append(h)

        place = 0
        x = 0
        list_of_answers = []
        for i in number_of_questions:
            list_cotation_3 = []
            if_true = []
            for v in questionnaire[x][1]:
                if v[1] == True:
                    if_true.append("True")
            x += 1
            num_quest = 1
            print(i, "\n")
            number_of_answers = []
            if len(if_true) == 1:
                for y in range(0, len(questionnaire[place][1])):
                    number_of_answers.append(questionnaire[place][1][y][0])
                    list_cotation_3.append([questionnaire[place][1][y][0]])
                list_pour_lesperance.append(list_cotation_3)
            elif len(if_true) != 1:
                check_list = []
                for y in range(0, len(questionnaire[place][1])):
                    number_of_answers.append(questionnaire[place][1][y][0])
                    check_list.append(questionnaire[place][1][y][0])
                taille = len(check_list) - len(if_true) +1
                while len(list_cotation_3) < taille:
                    list_cotation_3.append("object")
                list_pour_lesperance.append(list_cotation_3)
            random.shuffle(number_of_answers)#Mélange la liste de réponse, pour les afficher de manières différentes a chaque tentative.
            for z in number_of_answers:
                print(str(num_quest)+":", z)
                num_quest += 1
            if len(if_true) == 1: #Cette partie permet de gerer les questions avec seulement une réponse.
                w = input("Answer ==> ")
                while w.isdigit() == False: #Verifie si l'input est bien un nombre
                    print("Ceci n'est pas un nombre")
                    w = input("Answer ==> ")
                w = int(w)
                while True:
                    try: #Gestion d'erreure de type indexError, si l'utilisateur rentre un nombre out of range.
                        question = number_of_answers[w - 1]
                        break
                    except IndexError:
                        print("Le numéro de réponse n'existe pas !")
                        w = input("Answer ==> ")
                        w = int(w)
                answer = 0
                for j in questionnaire[place][1]:
                        if j[0] == question:
                            answer = j[1]
                if answer == True: #Si la réponse donné est correcte, affiche "Bonne réponse" en vert
                    sleep(0.2)
                    color("Bonne réponse !", "green")
                    print("-----------------------------------------------------------------------------")
                    list_of_answers.append(answer)
                else: #Si la réponse est fausse, affiche "Mauvaise réponse..." en rouge.
                    sleep(0.2)
                    color("Mauvaise réponse...", "red")
                    print("-----------------------------------------------------------------------------")
                    list_of_answers.append(answer)
                place += 1
            elif len(if_true) != 1: #Gère les réponses avec plusieurs réponse possible.
                listing = []
                print("Il y'a plusieurs réponses possibles à cette question, entrez toutes les réponses exactes pour avoir juste !")
                print("Entrez 'YES' si vous pensez avoir toutes les réponses; autrement , entrez une réponse supplémentaire. Si vous avez entré une réponse par erreur, tappez 'REMOVE'")
                while True:
                    s = input("Answer ==> ")
                    s = s.lower()
                    if s == "yes":
                        break
                    elif s == "remove" and len(listing) != 0:#Retire le dernier nombre input de la liste des réponses donné.
                        remove = listing[len(listing) - 1]
                        listing.remove(remove)
                        print(f"Vos réponses actuelles : {listing}")
                    elif s.isnumeric() == True and int(s) <= len(number_of_answers) and int(s) > 0:
                        s = int(s)
                        if s in listing:
                            print("Reponse déjà donnée !")
                        else:
                            listing.append(s)
                            print(f"Vos réponses actuelles : {listing}")
                    else:
                        print("Ceci n'est pas un nombre, ou alors le numéro de réponse n'existe pas, ou bien vous faites une commande qui n'a pas d'effet ou est incorrect !")
                # donc si la taille des réponses données = la taille des true
                if len(listing) == len(if_true):
                    #on check pour chacune de nos réponses
                    list_if_true = []
                    for i in listing:
                        i = int(i)
                        question = number_of_answers[i - 1]
                        answer = 0
                        for j in questionnaire[place][1]:
                            if j[0] == question:
                                answer = j[1]
                        if answer == True:
                            list_if_true.append(answer)
                    if len(list_if_true) == len(if_true):#Si la réponse donné est correcte, affiche "Bonne réponse" en vert
                        answer = True
                        sleep(0.2)
                        color("Bonne réponse !", "green")
                        print("-----------------------------------------------------------------------------")
                        list_of_answers.append(answer)
                    else: #Si la réponse est fausse, affiche "Mauvaise réponse..." en rouge.
                        answer = False
                        sleep(0.2)
                        color("Mauvaise réponse...Soit c'est la mauvaise réponse, soit vous n'avez pas trouvé TOUTES les réponses possibles ! ", "red")
                        print("-----------------------------------------------------------------------------")
                        list_of_answers.append(answer)
                elif len(listing) != len(if_true):
                    answer = False
                    sleep(0.2)
                    color("Mauvaise réponse...", "red")
                    print("-----------------------------------------------------------------------------")
                    list_of_answers.append(answer)

                place += 1
        if a == 0:  #Permet de d'utiliser le bon systemes de cotations en fonctions de ce que l'utilisateur a choisis
            resultat_final(cotation1(list_of_answers), questionnaire)
        elif a == 1:
            resultat_final(cotation2(list_of_answers), questionnaire)
        elif a == 2:
            resultat_final(cotation3(list_of_answers, list_pour_lesperance), questionnaire)
        while True: # Affichage des points avec tous les systemes de cotations
            results = input("Voulez-vous voir vos résultats selon les autres systèmes de cotation ? y/n \n")
            if results == "y":
                if a == 0:
                    print("Selon la cotation 2 : ")
                    resultat_final(cotation2(list_of_answers), questionnaire)
                    print("\n")
                    print("Selon la cotation 3 : ")
                    resultat_final(cotation3(list_of_answers, list_pour_lesperance), questionnaire)
                    print("\n")
                    break
                elif a == 1:
                    print("Selon la cotation 1 : ")
                    resultat_final(cotation1(list_of_answers), questionnaire) 
                    print("\n")
                    print("Selon la cotation 3 : ")
                    resultat_final(cotation3(list_of_answers, list_pour_lesperance), questionnaire)
                    print("\n")
                    break
                elif a == 2:
                    print("Selon la cotation 1 : ")
                    resultat_final(cotation1(list_of_answers), questionnaire)
                    print("\n")
                    print("Selon la cotation 2 : ")
                    resultat_final(cotation2(list_of_answers), questionnaire)
                    print("\n")
                    break
            elif results == "n":
                break

        while True:# Affiche toutes les bonne réponses si l'utilisateurs le souhaite.
            voircorr = input("Voulez-vous voir le correctif de ce QCM ? y/n")
            if voircorr == "y":
                correctif(questionnaire)
                break
            elif voircorr == "n":
                print("D'accord !")
                break
            else:
                print("Ceci n'est pas une réponse !") #Affiche ce message si l'input ne correspond pas.
        print("Voulez-vous refaire une partie ? y/n")
        retry = input("==> ")

        if retry.lower() == "y": #Commande qui permet de refaire une partie ou non.
            run = True  
        elif retry.lower() == "n":
            print("Merci d'avoir joué !")
            time.sleep(2)
            run = False
            break

Quizz()