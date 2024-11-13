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
        """     #Tristan
        @description : 
            Met à jour le niveau de révision ('review_level') de l'objet en fonction de la réponse de l'utilisateur.
            Ajuste la date de la prochaine révision ('next_review_date') en fonction du niveau de révision atteint

        @pré:
            * 'self.review_level' ets un entier supérieur ou égal à zéro. Il représente le niveau de révision actuel d'une carte
            * 'self.next_review_date' est de type 'datetime', il représente la date de la prochaine révision

        @post:
            * Si 'correct' est True, 'self.review_level' va être incrémenter de 1
            * Si `correct` est False et que `self.review_level` est plus grand ou égal à 1, `self.review_level` est décrémenté de 1.
            * `self.next_review_date` est mis à jour pour être la date actuelle plus `2 ** self.review_level` jours.
        """
        if correct:
            self.review_level += 1
        elif self.review_level >= 1:
            self.review_level -= 1

        self.next_review_date = datetime.now() + timedelta(days=2 ** self.review_level)  # ajuste la prochaine révision par rapport au niveau de connaissance

    def evaluate_response(self, user_response : str, correct_answer : str):
        """     #Tristan
        @description:
            Évalue la réponse donnée par l'utilisateur pour une carte en la comparant avec la bonne réponse
        
        @pré:
            * 'user_response' est un str qui représentela réponse donnée par le user
            * 'correct_answer' est un str qui représente la réponse correcte

        @post:
            * Retourne True si 'user_response' correspond à 'correct_answer'
            * Retourne False si 'user_response' ne correspond pas à 'correct_answer'
        """
        pass

class Set:  # ajout de la classe set pour regrouper les cards, à ajouter dans l'uml
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_flashcard(self, flashcard: Flashcard):
        """     #Tristan
        @description:
            Ajoute une nouvelle flashcard à la liste des cartes dans le set
        
        @pre:
            * 'flashcard' est une instance de la classe Flashcard qui contient une question et une réponse(plus un titre et le set correspondant)
            * 'self.cards' est une liste de flashcards déjà initialisée
        
        @post:
            * 'flashcard' est ajoutée à la liste 'self.cards'.
        """
        self.cards.append(flashcard)

class Statistics:
    def __init__(self):
        self.cards_reviewed = 0
        self.correct_answers = 0

    def calculate_progress(self, correct: bool):
        """     #Tristan
        @description:
            Met à jour les statistiques de révision
        
        @pre:
            * 'correct' est un booléen qui indique si la réponse est correcte
            * 'self.cards_reviewed' et 'self.correct_answers' sont des entiers initialisés pour suivre la progression de l'utilisateur
        
        @post:
            * 'self.cards_reviewed' est incrémenté de 1
            * 'self.correct_answers' est incrémenté de 1 si correct est True
        """
        self.cards_reviewed += 1
        if correct:
            self.correct_answers += 1

    def generate_graphics(self):
        """     #Tristan
        @description:
            Génère des graphiques de progression basés sur l'avancement de l'utilisateur
        
        @pre:
            * Les statistiques de progression ('self.cards_reviewed' et 'self.correct_answers') doivent être à jour
        
        @post:
            * Un graphique de progression est généré et affiché dans l'interface de l'application
            * Le graphique reflète les données actuelles des réponses correctes et du nombre total de cartes révisées
        """
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
        self.sets = self.import_flashcards_from_csv("listes.csv")
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
            with open("listes.csv", mode='a', encoding='utf-8', newline='') as file:
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

class UI:
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        # Initialisation de l'interface utilisateur
        self.window.title('FlashCards')
        self.window.geometry('1920x1080')
        self.window.minsize(600, 900)
        self.window.iconbitmap('images/logobidon.ico')
        self.window.config(background='white')

        self.titleFrame = Frame(self.window, bg='white')
        self.titleFrame.pack(expand=True)

        self.label_title = Label(self.titleFrame, text='Bienvenue Mr Jean-Révise', font=('Courier New', 30), bg="white", fg='black')
        self.label_title.pack()

        self.frame = Frame(self.window, bg='white')
        self.frame.pack(expand=True)

        self.set_choice = StringVar(self.frame)
        self.set_choice.set("Choisir un set")

        self.set_menu = ttk.Combobox(self.frame, textvariable=self.set_choice, values=list(self.app.sets.keys()))
        self.set_menu.pack(pady=10)
        self.set_menu.config(width=20)

        self.canvas = Canvas(self.frame, width=400, height=300, bg='white')
        self.canvas.pack(pady=20)

        self.start_button = Button(self.frame, text="Commencer la révision", command=self.start_revision, bg='blue', fg='white')
        self.start_button.pack(pady=5)

        self.toggle_button = Button(self.window, text='Mode Sombre', command=self.toggle_mode, bg='lightgray', fg='black')
        self.toggle_button.place(relx=1.0, rely=0.0, anchor='ne')

        self.question_label = Label(self.frame, text="", font=('Courier New', 20), bg="white", fg="black")
        self.question_label.pack()

        self.button_frame = Frame(self.frame, bg="white")
        self.button_frame.pack(pady=20)

        self.answer_button = Button(self.button_frame, text="Montrer la réponse", command=None, bg='lightgray')
        self.answer_button.grid(row=0, column=1, padx=5, pady=1)

        self.correct_button = Button(self.button_frame, text="Correct", command=None, bg='green')
        self.correct_button.grid(row=0, column=0, padx=5, pady=5)

        self.incorrect_button = Button(self.button_frame, text="Incorrect", command=None, bg='red')
        self.incorrect_button.grid(row=0, column=2, padx=5, pady=5)

        self.stats_label = Label(self.frame, text=self.app.stats.display(), font=('Courier New', 12), bg="white", fg="black")
        self.stats_label.pack()

        self.add_card_frame = Frame(self.frame, bg="white")
        self.add_card_frame.pack(pady=10)

        Label(self.add_card_frame, text="Question:", font=('Courier New', 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.question_entry = Entry(self.add_card_frame, font=('Courier New', 12), width=30)
        self.question_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(self.add_card_frame, text="Réponse:", font=('Courier New', 12), bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.answer_entry = Entry(self.add_card_frame, font=('Courier New', 12), width=30)
        self.answer_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(self.add_card_frame, text="Titre:", font=('Courier New', 12), bg="white").grid(row=2, column=0, padx=5, pady=5)
        self.title_entry = Entry(self.add_card_frame, font=('Courier New', 12), width=30)
        self.title_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(self.add_card_frame, text="Set:", font=('Courier New', 12), bg="white").grid(row=3, column=0, padx=5, pady=5)
        self.set_entry = Entry(self.add_card_frame, font=('Courier New', 12), width=30)
        self.set_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = Button(self.add_card_frame, text="Ajouter une flashcard", command=self.add_flashcard, bg='orange')
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def toggle_mode(self):
        if self.window.cget('bg') == 'white':
            # Mode sombre
            self.window.config(background='black')
            self.titleFrame.config(background='black')
            self.frame.config(background='black')
            self.label_title.config(bg='black', fg='white')
            self.set_menu.config(background='gray', foreground='white')
            self.canvas.config(bg='black')
            self.start_button.config(bg='darkgray', fg='white')
            self.toggle_button.config(bg='gray', fg='white', text='Mode Clair')
            self.question_label.config(bg='black', fg='white')
            self.button_frame.config(bg='black')
            self.answer_button.config(bg='darkgray', fg='white')
            self.correct_button.config(bg='darkgreen', fg='white')
            self.incorrect_button.config(bg='darkred', fg='white')
            self.stats_label.config(bg='black', fg='white')
            self.add_card_frame.config(bg='black')
            self.question_entry.config(bg='gray', fg='white')
            self.answer_entry.config(bg='gray', fg='white')
            self.title_entry.config(bg='gray', fg='white')
            self.set_entry.config(bg='gray', fg='white')
            self.add_button.config(bg='darkorange', fg='white')

            if not self.set_menu.get():
                self.set_menu.set('Choisir un set')

        else:
            # Mode clair
            self.window.config(background='white')
            self.titleFrame.config(background='white')
            self.frame.config(background='white')
            self.label_title.config(bg='white', fg='black')
            self.set_menu.config(background='white', foreground='black')
            self.canvas.config(bg='white')
            self.start_button.config(bg='blue', fg='white')
            self.toggle_button.config(bg='lightgray', fg='black', text='Mode Sombre')
            self.question_label.config(bg='white', fg='black')
            self.button_frame.config(bg='white')
            self.answer_button.config(bg='lightgray', fg='black')
            self.correct_button.config(bg='green', fg='black')
            self.incorrect_button.config(bg='red', fg='black')
            self.stats_label.config(bg='white', fg='black')
            self.add_card_frame.config(bg='white')
            self.question_entry.config(bg='white', fg='black')
            self.answer_entry.config(bg='white', fg='black')
            self.title_entry.config(bg='white', fg='black')
            self.set_entry.config(bg='white', fg='black')
            self.add_button.config(bg='orange', fg='black')

            if not self.set_menu.get():
                self.set_menu.set('Choisir un set')

    def start_revision(self):
        selected_set_name = self.set_choice.get()
        current_set = self.app.sets.get(selected_set_name)
        if current_set and current_set.cards:
            current_card = random.choice(current_set.cards)
            self.show_card(current_card)
        else:
            self.question_label.config(text="Aucune carte disponible dans ce set.")

    def show_card(self, card):
        self.canvas.delete("all")
        self.draw_card(self.canvas, card, 50, 50, 300, 200)
        self.answer_button.config(command=lambda: self.show_answer(card))

    def show_answer(self, card):
        self.canvas.delete("all")
        self.draw_card(self.canvas, card, 50, 50, 300, 200, answer=True)
        self.correct_button.config(command=lambda: self.evaluate(card, True))
        self.incorrect_button.config(command=lambda: self.evaluate(card, False))

    def evaluate(self, card, correct):
        card.review(correct)
        self.app.stats.calculate_progress(correct)
        self.stats_label.config(text=self.app.stats.display())
        self.start_revision()

    def update_set_menu(self):
        self.set_menu['values'] = list(self.app.sets.keys())
        if not self.set_menu.get():
            self.set_menu.set('Choisir un set')

    def draw_card(self, canvas, card, x, y, width, height, answer=False):
        canvas.create_rectangle(x, y, x + width, y + height, fill='lightblue', outline='black')
        if answer:
            text = f"Réponse: {card.answer}"
        else:
            text = card.question

        canvas.create_text(x + width / 2, y + height / 2, text=text, font=('Courier New', 16), fill='black')

    def add_flashcard(self):
        title = self.title_entry.get()
        question = self.question_entry.get()
        answer = self.answer_entry.get()
        set_name = self.set_entry.get()

        if title and question and answer and set_name:
            self.app.create_flashcard(title, question, answer, set_name)
            self.update_set_menu()
            self.title_entry.delete(0, END)
            self.question_entry.delete(0, END)
            self.answer_entry.delete(0, END)
            self.set_entry.delete(0, END)

# Créer une instance de l'application
app = Application(app_name='FlashCards', version='1.0')

# Créer fenêtre
window = Tk()

# Créer une instance de l'interface utilisateur
ui = UI(window, app)

# Lancer la fenêtre
window.mainloop()
