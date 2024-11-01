from tkinter import *

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

# Créer fenêtre
window = Tk()

# Modifier fenêtre
window.title('FlashCards')
window.geometry('1920x1080')
window.minsize(480, 360)
#window.iconbitmap('../images/logobidon.ico')  # jsp pourquoi ca va pas ....
window.config(background='white')  # Changer la couleur de fond

#créer une 'frame', un cadre pour contenir les éléments
frame = Frame(window, bg='white')
frame.pack(expand=True)

# Ajouter un bouton pour changer de mode
toggle_button = Button(window, text='Mode Sombre', command=toggle_mode, bg='lightgray', fg='black')
toggle_button.place(relx=1.0, rely=0.0, anchor='ne')  # Positionner le bouton en haut à droite

# Ajouter du texte
label_title = Label(frame, text='Bienvenue Mr Jean-Révise', font=('Courier New', 30), bg="white", fg='black')
label_title.pack()

# Ajouter du texte
label_subtitle = Label(frame, text='test', font=('Courier New', 20), bg="white", fg='black')
label_subtitle.pack()

# Afficher
window.mainloop()

import os
print(os.getcwd())





#création des classes


from datetime import date, time
from typing import List
import csv #pour les flashcards sur excel ???


class Flashcard:
    def __init__(self, title: str, content: str, review_level: int):
        pass

    def review(self):
        pass

    def evaluate_response(self):
        pass

class Statistics:
    def __init__(self, cards_reviewed: int, progress: int):
        pass

    def calculate_progress(self):
        pass

    def generate_graphics(self):
        pass

class Badge:
    def __init__(self, name: str, description: str, attainment_conditions: str):
        pass

    def assign_badge(self):
        pass

class Reminder:
    def __init__(self, reminder_date: date, reminder_time: time, cards_to_review: List[Flashcard]):
        pass

    def send_reminder(self):
        pass

class Application:
    def __init__(self, app_name: str, version: str):
        pass

    def create_flashcard(self, title: str, content: str, review_level: int):
        pass

    def display_statistics(self):
        pass

    def send_reminder(self, reminder_date: date, reminder_time: time, cards_to_review: List[Flashcard]):
        pass

    def unlock_badge(self, badge: Badge):
        pass

    def import_flashcards_from_csv(self, file_path: str):   # a ajouter si on prend ca d'un excel ?? mais va avec create_flashcard 
        pass