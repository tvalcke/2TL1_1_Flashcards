#### page pour réécrire le code et tester sans risquer de péter le principal #####

from tkinter import *
from tkinter import ttk #je l'importe en plus car il n'est pas compris dans *

from datetime import date, time, datetime, timedelta
from typing import List, Dict
import csv
import random
import os

print(os.getcwd())

# Classes
class Flashcard:
    def __init__(self, title: str, question: str, answer: str, review_level: int = 0):
        self.title = title
        self.question = question
        self.answer = answer
        self.review_level = review_level
        self.next_review_date = datetime.now()  # sera pour réévaluer la prochaine révision

    def review(self, correct: bool):
        if correct:
            self.review_level += 1
        elif self.review_level >= 1:
            self.review_level -= 1

        self.next_review_date = datetime.now() + timedelta(days=2 ** self.review_level)  # ajuste la prochaine révision par rapport au niveau de connaissance

    def evaluate_response(self):
        pass

class Set:  # ajout de la classe set pour regrouper les cards, à ajouter dans l'uml
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_flashcard(self, flashcard: Flashcard):
        self.cards.append(flashcard)

class Statistics:
    def __init__(self):
        self.cards_reviewed = 0
        self.correct_answers = 0

    def calculate_progress(self, correct: bool):
        self.cards_reviewed += 1
        if correct:
            self.correct_answers += 1

    def generate_graphics(self):
        pass

    def display(self):  # sert pour le mvp, pas encore besoin de generate_graphics
        if self.cards_reviewed > 0:
            accuracy = (self.correct_answers / self.cards_reviewed) * 100
        else:
            accuracy = 0
        return ("Nombre de cartes vues: ", self.cards_reviewed, ", précision: ", round(accuracy, 2), " %. ")

class Badge:
    def __init__(self, name: str, description: str, attainment_conditions: str):
        self.name = name
        self.description = description
        self.attainment_conditions = attainment_conditions

    def assign_badge(self):
        pass

class Reminder:
    def __init__(self, reminder_date: date, reminder_time: time, cards_to_review: List[Flashcard]):
        self.reminder_date = reminder_date
        self.reminder_time = reminder_time
        self.cards_to_review = cards_to_review

    def send_reminder(self):
        pass

class Application:
    def __init__(self, app_name: str, version: str):
        self.app_name = app_name
        self.version = version
        self.sets = self.import_flashcards_from_csv("C:/Users/valck/Desktop/Ephec/BAC2/dev2/2TL1_1_Flashcards/listes.csv")
        self.stats = Statistics()

    def import_flashcards_from_csv(self, file_path: str):
        sets = {}
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)

                for i in reader:
                    if len(i) < 4:  # Si la ligne n'a pas assez de colonnes
                        continue

                    title, question, answer, set_name = i[0], i[1], i[2], i[3]

                    if set_name not in sets:  # Si le set n'existe pas encore
                        sets[set_name] = Set(set_name)

                    sets[set_name].add_flashcard(Flashcard(title, question, answer))

            return sets

        except FileNotFoundError:  # fichier pas trouvé
            print("Le fichier n'a pas été trouvé à l'emplacement spécifié.")
            return sets

        except UnicodeDecodeError:  # Si mauvais encodage
            print("Erreur de décodage du fichier avec l'encodage UTF-8. Vérifie l'encodage.")

        return sets  # si on n'a pas pu lire ça, renvoie les sets vides

    def create_flashcard(self, title: str, question: str, answer: str, set_name: str):
        if set_name not in self.sets:  # Vérifie si le set existe sinon on le crée
            self.sets[set_name] = Set(set_name)
        
        new_card = Flashcard(title, question, answer)   # créer la carte
        self.sets[set_name].add_flashcard(new_card)
        print("Flashcard '" + title + "' ajoutée dans le set '" + set_name + "'.")
        
        # Ajoute la flashcard au fichier CSV
        try:
            with open("C:/Users/valck/Desktop/Ephec/BAC2/dev2/2TL1_1_Flashcards/listes.csv", mode='a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title, question, answer, set_name])
        except Exception as e:
            print("Erreur lors de l'écriture dans le fichier CSV :", e)

    def display_statistics(self):
        pass

    def send_reminder(self, reminder_date: date, reminder_time: time, cards_to_review: List[Flashcard]):
        pass

    def unlock_badge(self, badge: Badge):
        pass

# Fonction pour basculer entre le mode sombre et clair
def toggle_mode():
    if window.config('bg')[-1] == 'white':  # Vérifie la couleur de fond actuelle
        window.config(background='black')
        frame.config(background='black')
        label_title.config(bg='black', fg='white')
        label_subtitle.config(bg='black', fg='white')
        toggle_button.config(bg='gray', fg='white', text='Mode Clair')
    else:
        window.config(background='white')
        frame.config(background='white')
        label_title.config(bg='white', fg='black')
        label_subtitle.config(bg='white', fg='black')
        toggle_button.config(bg='lightgray', fg='black', text='Mode Sombre')

def start_revision():
    selected_set_name = set_choice.get()  # Récupère le nom du set choisi dans le menu déroulant
    current_set = app.sets.get(selected_set_name)
    if current_set and current_set.cards:
        current_card = random.choice(current_set.cards)
        show_card(current_card)
    else:
        question_label.config(text="Aucune carte disponible dans ce set.")

def show_card(card):
    question_label.config(text=card.question)
    answer_button.config(command=lambda: show_answer(card))

def show_answer(card):
    question_label.config(text=f"Réponse: {card.answer}")
    correct_button.config(command=lambda: evaluate(card, True))
    incorrect_button.config(command=lambda: evaluate(card, False))

def evaluate(card, correct):
    card.review(correct)  # Applique l’algorithme SRS basique
    app.stats.calculate_progress(correct)
    stats_label.config(text=app.stats.display())
    start_revision()

# Créer une instance de l'application
app = Application(app_name='FlashCards', version='1.0')

# Créer fenêtre
window = Tk()

# Modifier fenêtre
window.title('FlashCards')
window.geometry('1920x1080')
window.minsize(480, 360)
# window.iconbitmap('../images/logobidon.ico')  # jsp pourquoi ça va pas .....
window.config(background='white')  # Changer la couleur de fond

# créer une 'frame', un cadre pour contenir les éléments
frame = Frame(window, bg='white')
frame.pack(expand=True)

# ici je crée un drop down menu pour choisir le set à étudier
set_choice = StringVar(window)
set_choice.set("Choisir un set")  # Valeur par défaut

# Initialisation de la liste des sets pour le menu déroulant
set_menu = ttk.Combobox(window, textvariable=set_choice, values=list(app.sets.keys()))
set_menu.place(relx=0.5, rely=0.1, anchor='n')  # Positionnement du menu déroulant
set_menu.config(width=20)

start_button = Button(frame, text="Commencer la révision", command=start_revision, bg='blue', fg='white')
start_button.pack(pady=20)

# Ajouter un bouton pour changer de mode
toggle_button = Button(window, text='Mode Sombre', command=toggle_mode, bg='lightgray', fg='black')
toggle_button.place(relx=1.0, rely=0.0, anchor='ne')  # Positionner le bouton en haut à droite

# Ajouter du texte
label_title = Label(frame, text='Bienvenue Mr Jean-Révise', font=('Courier New', 30), bg="white", fg='black')
label_title.pack()

# Ajouter du texte
label_subtitle = Label(frame, text='test', font=('Courier New', 20), bg="white", fg='black')
label_subtitle.pack()

# Interface utilisateur pour la révision
question_label = Label(frame, text="", font=('Courier New', 20), bg="white", fg="black")
question_label.pack()
answer_button = Button(frame, text="Montrer la réponse", command=None, bg='lightgray')
answer_button.pack()
correct_button = Button(frame, text="Correct", command=None, bg='green')
correct_button.pack(side=LEFT, padx=5, pady=5)
incorrect_button = Button(frame, text="Incorrect", command=None, bg='red')
incorrect_button.pack(side=RIGHT, padx=5, pady=5)

# Statistiques minimales
stats_label = Label(frame, text=app.stats.display(), font=('Courier New', 12), bg="white", fg="black")
stats_label.pack()

# Ajouter un formulaire pour créer une nouvelle flashcard
add_card_frame = Frame(frame, bg="white")
add_card_frame.pack(pady=10)

Label(add_card_frame, text="Question:", font=('Courier New', 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
question_entry = Entry(add_card_frame, font=('Courier New', 12), width=30)
question_entry.grid(row=0, column=1, padx=5, pady=5)

Label(add_card_frame, text="Réponse:", font=('Courier New', 12), bg="white").grid(row=1, column=0, padx=5, pady=5)
answer_entry = Entry(add_card_frame, font=('Courier New', 12), width=30)
answer_entry.grid(row=1, column=1, padx=5, pady=5)

Label(add_card_frame, text="Titre:", font=('Courier New', 12), bg="white").grid(row=2, column=0, padx=5, pady=5)
title_entry = Entry(add_card_frame, font=('Courier New', 12), width=30)
title_entry.grid(row=2, column=1, padx=5, pady=5)

Label(add_card_frame, text="Set:", font=('Courier New', 12), bg="white").grid(row=3, column=0, padx=5, pady=5)
set_entry = Entry(add_card_frame, font=('Courier New', 12), width=30)
set_entry.grid(row=3, column=1, padx=5, pady=5)

def add_flashcard():
    title = title_entry.get()
    question = question_entry.get()
    answer = answer_entry.get()
    set_name = set_entry.get()

    if title and question and answer and set_name:  # vérifie que tous les champs sont remplis
        app.create_flashcard(title, question, answer, set_name)
        title_entry.delete(0, END)
        question_entry.delete(0, END)
        answer_entry.delete(0, END)
        set_entry.delete(0, END)

add_button = Button(add_card_frame, text="Ajouter une flashcard", command=add_flashcard, bg='orange')
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Lancer la fenêtre
window.mainloop()
