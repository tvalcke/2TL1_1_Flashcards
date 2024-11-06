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
        return "Nombre de cartes vues: " + str(self.cards_reviewed) + ", précision: " + str(round(accuracy, 2)) + " %."


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
    if window.cget('bg') == 'white':  # Vérifie la couleur de fond actuelle
        # Mode sombre
        window.config(background='black')
        titleFrame.config(background='black')
        frame.config(background='black')
        label_title.config(bg='black', fg='white')
        set_menu.config(background='gray', foreground='white')
        canvas.config(bg='black')
        start_button.config(bg='darkgray', fg='white')
        toggle_button.config(bg='gray', fg='white', text='Mode Clair')
        question_label.config(bg='black', fg='white')
        button_frame.config(bg='black')
        answer_button.config(bg='darkgray', fg='white')
        correct_button.config(bg='darkgreen', fg='white')
        incorrect_button.config(bg='darkred', fg='white')
        stats_label.config(bg='black', fg='white')
        add_card_frame.config(bg='black')
        question_entry.config(bg='gray', fg='white')
        answer_entry.config(bg='gray', fg='white')
        title_entry.config(bg='gray', fg='white')
        set_entry.config(bg='gray', fg='white')
        add_button.config(bg='darkorange', fg='white')

        if not set_menu.get():  #refresh le ddm pour afficher qlq chose si aucun set n'ets choisit 
            set_menu.set('Choisir un set')
        
    else:
        # Mode clair
        window.config(background='white')
        titleFrame.config(background='white')
        frame.config(background='white')
        label_title.config(bg='white', fg='black')
        set_menu.config(background='white', foreground='black')
        canvas.config(bg='white')
        start_button.config(bg='blue', fg='white')
        toggle_button.config(bg='lightgray', fg='black', text='Mode Sombre')
        question_label.config(bg='white', fg='black')
        button_frame.config(bg='white')
        answer_button.config(bg='lightgray', fg='black')
        correct_button.config(bg='green', fg='black')
        incorrect_button.config(bg='red', fg='black')
        stats_label.config(bg='white', fg='black')
        add_card_frame.config(bg='white')
        question_entry.config(bg='white', fg='black')
        answer_entry.config(bg='white', fg='black')
        title_entry.config(bg='white', fg='black')
        set_entry.config(bg='white', fg='black')
        add_button.config(bg='orange', fg='black')

        if not set_menu.get():
            set_menu.set('Choisir un set')



def start_revision():
    selected_set_name = set_choice.get()  # on récupère ce qu'on a choisit dans le drop down menu
    current_set = app.sets.get(selected_set_name)
    if current_set and current_set.cards:
        current_card = random.choice(current_set.cards)
        show_card(current_card)
    else:
        question_label.config(text="Aucune carte disponible dans ce set.")

def show_card(card):
    canvas.delete("all")
    draw_card(canvas, card, 50, 50, 300, 200)  # Dessiner la carte
    answer_button.config(command=lambda: show_answer(card))


def show_answer(card):
    canvas.delete("all") 
    draw_card(canvas, card, 50, 50, 300, 200, answer=True)
    correct_button.config(command=lambda: evaluate(card, True))
    incorrect_button.config(command=lambda: evaluate(card, False))


def evaluate(card, correct):
    card.review(correct)  # Applique l’algorithme SRS basique
    app.stats.calculate_progress(correct)
    stats_label.config(text=app.stats.display())
    start_revision()

def update_set_menu():  #sert quand on ajoute un set inexistant, pour refresh le drop down menu
    set_menu['values'] = list(app.sets.keys())
    if not set_menu.get(): 
        set_menu.set('Choisir un set') 

def draw_card(canvas, card, x, y, width, height, answer=False):
    canvas.create_rectangle(x, y, x + width, y + height, fill='lightblue', outline='black')
    if answer:
        text = f"Réponse: {card.answer}"
    else:
        text = card.question

    canvas.create_text(x + width / 2, y + height / 2, text=text, font=('Courier New', 16), fill='black')


# Créer une instance de l'application
app = Application(app_name='FlashCards', version='1.0')

# Créer fenêtre
window = Tk()

# Créer un style pour le menu déroulant
style = ttk.Style()
style.configure("TCombobox", fieldbackground="white", foreground="black")


# Modifier fenêtre
window.title('FlashCards')
window.geometry('1920x1080')
window.minsize(600, 900)
# window.iconbitmap('../images/logobidon.ico')  # jsp pourquoi ça va pas .....
window.config(background='white')  # Changer la couleur de fond

# créer une 'frame', un cadre pour contenir les éléments
titleFrame = Frame(window, bg='white')
titleFrame.pack(expand=True)

# Ajouter du texte
label_title = Label(titleFrame,text='Bienvenue Mr Jean-Révise', font=('Courier New', 30), bg="white", fg='black')
label_title.pack()

# créer une 'frame', un cadre pour contenir les éléments
frame = Frame(window, bg='white')
frame.pack(expand=True)

# ici je crée un drop down menu pour choisir le set à étudier
set_choice = StringVar(frame)
set_choice.set("Choisir un set")  # Valeur par défaut

# Initialisation de la liste des sets pour le menu déroulant
set_menu = ttk.Combobox(frame, textvariable=set_choice, values=list(app.sets.keys()))
set_menu.pack(pady=10)
set_menu.config(width=20)

# Canvas qui dessine les cards
canvas = Canvas(frame, width=400, height=300, bg='white')
canvas.pack(pady=20)

start_button = Button(frame, text="Commencer la révision", command=start_revision, bg='blue', fg='white')
start_button.pack(pady=20)

# Ajouter un bouton pour changer de mode
toggle_button = Button(window, text='Mode Sombre', command=toggle_mode, bg='lightgray', fg='black')
toggle_button.place(relx=1.0, rely=0.0, anchor='ne')  # Positionner le bouton en haut à droite

# Interface utilisateur pour la révision
question_label = Label(frame, text="", font=('Courier New', 20), bg="white", fg="black")
question_label.pack()

# Créer un cadre pour les boutons
button_frame = Frame(frame, bg="white")
button_frame.pack(pady=20)

answer_button = Button(button_frame, text="Montrer la réponse", command=None, bg='lightgray')
answer_button.grid(row=0, column=1, padx=5, pady=5)

correct_button = Button(button_frame, text="Correct", command=None, bg='green')
correct_button.grid(row=0, column=0, padx=5, pady=5)

incorrect_button = Button(button_frame, text="Incorrect", command=None, bg='red')
incorrect_button.grid(row=0, column=2, padx=5, pady=5)


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
        update_set_menu()  # réactualise le drop down
        title_entry.delete(0, END)
        question_entry.delete(0, END)
        answer_entry.delete(0, END)
        set_entry.delete(0, END)


add_button = Button(add_card_frame, text="Ajouter une flashcard", command=add_flashcard, bg='orange')
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Lancer la fenêtre
window.mainloop()
