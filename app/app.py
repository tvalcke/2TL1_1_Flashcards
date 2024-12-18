"""
Code rédigé par Préat Thomas - Hertmans Mathéo - Valcke Tristan - Colson Nathan
Dans le cadre du cours de DEV2 en 2ème année de bachelier de TI à l'EPHEC

Chat GPT a été utilisé pour trouver un modèle de commentaires pour les méthodes
"""
from tkinter import Tk
from tkinter import ttk
from tkinter import Label
from tkinter import Frame
from tkinter import StringVar
from tkinter import Canvas
from tkinter import Button
from tkinter import Entry
from tkinter import Menu
from tkinter import messagebox
from tkinter import END

from datetime import date, time, datetime, timedelta
from typing import List
import csv
import random


class Flashcard:
    def __init__(self, title: str, question: str, answer: str,
                 review_level: int = 0):
        self.title = title
        self.question = question
        self.answer = answer
        self.review_level = review_level
        # Réévaluer la prochaine révision:
        self.next_review_date = datetime.now()
        # self.image_front  = image_front
        # self.image_back  = image_back

    def review(self, correct: bool):
        """     #Tristan
        @description :
            Met à jour le niveau de révision ('review_level') de l'objet
            en fonction de la réponse de l'utilisateur.
            Ajuste la date de la prochaine révision ('next_review_date')
            en fonction du niveau de révision atteint

        @pré:
            * 'self.review_level' ets un entier supérieur ou égal à zéro.
            Il représente le niveau de révision actuel d'une carte
            * 'self.next_review_date' est de type 'datetime', il représente la
            date de la prochaine révision

        @post:
            * Si 'correct' est True, 'self.review_level' va être incrémenter
            de 1
            * Si `correct` est False et que `self.review_level` est plus grand
            ou égal à 1, `self.review_level` est décrémenté de 1.
            * `self.next_review_date` est mis à jour pour être la
            date actuelle plus `2 ** self.review_level` jours.
        """
        if correct:
            self.review_level += 1
        elif self.review_level >= 1:
            self.review_level -= 1
        # ajuste la prochaine révision par rapport au niveau de connaissance :
        try:
            self.next_review_date = datetime.now() + timedelta(
                days=2 ** self.review_level
            )
        except OverflowError as e:
            raise ValueError(
                "Review level trop élevé pour être calculé."
            ) from e

    def evaluate_response(self, user_response: str, correct_answer: str):
        """     #Tristan
        @description:
            Évalue la réponse donnée par l'utilisateur pour une carte en la
            comparant avec la bonne réponse
        @pré:
            * 'user_response' est un str qui représentela réponse donnée par
            le user
            * 'correct_answer' est un str qui représente la réponse correcte
        @post:
            * Retourne True si 'user_response' correspond à 'correct_answer'
            * Retourne False si 'user_response' ne correspond
            pas à 'correct_answer'
        """
        pass


class Group:
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_flashcard(self, flashcard: Flashcard):
        """     #Tristan
        @description:
            Ajoute une nouvelle flashcard à la liste des cartes dans le set
        @pre:
            * 'self.cards' est une liste de flashcards déjà initialisée
        @post:
            * 'flashcard' est ajoutée à la liste 'self.cards'.
        """
        if not isinstance(flashcard, Flashcard):
            raise TypeError(
                "L'objet doit être une instance de la classe Flashcard."
            )

        self.cards.append(flashcard)


class Mode:
    def __init__(self, mode_type: str, time_limit: int, review_order: str):
        self.mode_type = mode_type
        self.time_limit = time_limit
        self.review_order = review_order

    def start_review(self):
        """ La fonction 'start_revision' se trouve dans la classe UI,
            est ce qu'il faudrait pas la mettre ici ? ou taper
            ca dans la clas app ? """
        pass

    def shuffle_cards(self):
        pass

    def end_review(self):
        pass


class Statistics:
    def __init__(self):
        self.cards_reviewed = 0
        self.correct_answers = 0
        self.user_xp = 0
        self.streak_count = 0.0
        self.badges = [
            Badge("Débutant", "Atteignez 100 XP.", 100),
            Badge("Intermédiaire", "Atteignez 250 XP.", 250),
            Badge("Expert", "Atteignez 500 XP.", 500),
            Badge("Maître", "Atteignez 1000 XP.", 1000),
        ]

    def calculate_Xp(self, streak_indicator):
        """     #Thomas
        @description:
            Met à jour les points d'expérience

        @pre:
            * 'streak_indicator' est un booléen qui indique
            si la réponse est correcte
            * 'streak_count' est un float >= 0, incrémenté de 0.1 par bonne
            réponse servant de multiplicateur d'xp
            * 'user_xp' est un float >= 0 initialisé pour suivre la
            progression de l'utilisateur

        @post:
            * 'user_xp' et 'streak_count' sont incrémentés si la
            réponse est bonne
            * 'user_xp' n'est pas incrémenté et 'streak_count' est remis à 1
            si la réponse est mauvaise
        """
        if not isinstance(streak_indicator, bool):
            raise ValueError("'streak_indicator' doit être un booléen.")

        if streak_indicator:
            self.user_xp += int(100 * (self.streak_count + 1))
            self.streak_count += 0.1
            try:
                self.unlock_badge()
            except Exception as e:
                raise RuntimeError(
                    "Erreur lors du déblocage des badges."
                ) from e
        else:
            self.streak_count = 0.0

    def unlock_badge(self):
        """
        Vérifie les badges non débloqués et assigne ceux dont le palier d'XP
        est atteint.
        """
        for badge in self.badges:
            if badge.check_criteria(self.user_xp):
                badge.assign_badge()
                print(self.user_xp)

    def send_badges(self):
        """
        Retourne le badge le plus élevé actuellement débloqué.
        """
        unlocked_badges = [badge for badge in self.badges if badge.earned]
        print("go")
        if unlocked_badges:
            # Retourner le badge avec le plus grand xp_threshold
            latest_badge = max(unlocked_badges, key=lambda b: b.xp_threshold)
            return str(latest_badge)
        return "Aucun badge débloqué pour le moment."

    def calculate_progress(self, correct: bool):
        """     #Tristan + Thomas
        @description:
            Met à jour les statistiques de révision
        @pre:
            * 'correct' est un booléen qui indique si la réponse est correcte
            * 'self.cards_reviewed' et 'self.correct_answers' sont des entiers
            initialisés pour suivre la progression de l'utilisateur
        @post:
            * 'self.cards_reviewed' est incrémenté de 1
            * 'self.correct_answers' est incrémenté de 1 si correct est True
            * appelle la méthode 'calculate_xp' pour mettre à jour l'expérience
        """
        if not isinstance(correct, bool):
            raise ValueError("'correct' doit être un booléen.")

        self.cards_reviewed += 1
        if correct:
            self.correct_answers += 1

        Statistics.calculate_Xp(self, correct)

    def generate_graphics(self):
        """     #Tristan
        @description:
            Génère des graphiques de progression basés sur l'avancement de
            l'utilisateur
        @pre:
            * Les statistiques de progression ('self.cards_reviewed' et
            'self.correct_answers') doivent être à jour
        @post:
            * Un graphique de progression est généré et affiché dans
            l'interface de l'application
            * Le graphique reflète les données actuelles des réponses
            correctes et du nombre total de cartes révisées
        """
        pass

    def send_stats(self):  # pour le mvp, pas encre besoin de generate_graphics
        """    #Thomas
        @description:
            Calcule et retourne un résumé des statistiques de révision.
        @pre:
            * 'cards_reviewed' est un entier >= 0 indiquant combien de cartes
            on été revues
            * 'correct_answers' est un entier >= 0 indiquant combien de bonnes
            réponses on été données
            * 'accuracy' est un float >= 0 indiquant le pourcentage de
            réussite de la session de révision actuelle
                il est calculé par le nombre de bonnes réponses divisé par le
                total de cartes revues
            * 'user_xp' est un entier >= 0 représentant le total de points
            d'expérience de l'utilisateur
            * 'streak_count est un float >= 0 utilisé pour calculer le nombre
            de cartes réussies d'affilée
        @post:
            * Retourne une chaîne décrivant le nombre de cartes vues, la
            précision en pourcentage, les points d'XP et le combo actuel.
            * Le combo actuel est égal à 'streak_count' * 10
        """
        if not isinstance(self.cards_reviewed, int) or not isinstance(
            self.correct_answers, int
        ):
            raise TypeError(
                "'cards_reviewed' et 'correct_answers' doivent"
                " être des entiers."
            )
        if self.cards_reviewed < 0 or self.correct_answers < 0:
            raise ValueError(
                "'cards_reviewed' et 'correct_answers' ne"
                "peuvent pas être négatifs."
                )

        if self.cards_reviewed > 0:
            accuracy = (self.correct_answers / self.cards_reviewed) * 100
        else:
            accuracy = 0

        return (
            f"Nombre de cartes vues: {self.cards_reviewed}, précision: {
                round(accuracy, 2)
            } %. \n\n"
            f"XP: {self.user_xp} Combo: {int(self.streak_count * 10)}"
        )


class Badge:
    def __init__(self, name: str, description: str,
                 xp_threshold: int, badge_icon=None):
        if not isinstance(name, str) or not isinstance(description, str):
            raise TypeError("Les paramètres 'name' et 'description' doivent "
                            "être des chaînes de caractères.")
        if not isinstance(xp_threshold, int) or xp_threshold < 0:
            raise ValueError("'xp_threshold' doit être un entier positif.")

        self.name = name
        self.description = description
        self.xp_threshold = xp_threshold
        self.badge_icon = badge_icon
        self.date_earned = None
        self.earned = False

    def check_criteria(self, user_xp: int):
        """
        @description :
            Verifie si le palier d'XP est atteint pour debloquer ce badge
        """
        if not isinstance(user_xp, int) or user_xp < 0:
            raise ValueError("'user_xp' doit être un entier positif.")
        return user_xp >= self.xp_threshold and not self.earned

    def assign_badge(self):
        """    #Thomas
        @description:
            Vérifie si les conditions d'obtention sont remplies et assigne
            un badge à l'utilisateur.
        @pre:
            * `attainment_conditions` est une chaîne qui décrit les
            conditions nécessaires.
        @post:
            * Attribue un badge si les conditions sont remplies
            (implémentation future).
        """
        if self.earned:
            raise RuntimeError("Ce badge a déjà été attribué.")

        try:
            self.date_earned = datetime.now().strftime("%d/%m/%Y %H:%M")
        except Exception as e:
            raise RuntimeError(
                "Erreur lors de l'attribution de la date."
            ) from e

        self.earned = True

    def __str__(self):
        if not self.date_earned:
            return (
                f"Badge: {self.name}, Description: {self.description}, "
                "Non encore attribué."
            )
        return (
            f"Badge: {self.name}, Description: {self.description}, "
            f"Date Earned: {self.date_earned}"
        )


class Reminder:
    def __init__(self, reminder_date: date, reminder_time: time,
                 cards_to_review: List[Flashcard], revision_history: list):
        self.reminder_date = reminder_date
        self.reminder_time = reminder_time
        self.cards_to_review = cards_to_review
        self.revision_history = revision_history

    def add_revision(self, date, result):
        pass

    def send_reminder(self):
        """     #Thomas
        @description:
            Envoie un rappel aux utilisateurs pour réviser les cartes de flash
            définies dans `cards_to_review`.
        @pre:
            * `self.reminder_date` et `self.reminder_time` sont de types `date`
            et `time`, définissant la date et l'heure du rappel.
            * `self.cards_to_review` est une liste de `Flashcard` contenant
            les cartes à réviser.
        @post:
            * Un rappel est déclenché, demandant à l'utilisateur de réviser
            les cartes dans `self.cards_to_review`.
            * Le rappel peut être affiché dans l'interface utilisateur ou
            envoyé par un autre moyen si spécifié.
        """
        pass

    def get_revision_history(self):
        pass


class Application:
    def __init__(self, app_name: str, version: str):
        self.app_name = app_name
        self.version = version
        self.sets = self.import_flashcards_from_csv("listes.csv")
        self.stats = Statistics()

    def import_flashcards_from_csv(self, file_path: str):
        """    #Thomas
        @description:
            Importe des flashcards depuis un fichier CSV et les ajoute aux
            ensembles de l'application.
        @pre:
            * `file_path` est le chemin d'un fichier CSV accessible.
        @post:
            * Retourne un dictionnaire de `Set` contenant les cartes importées.
            * Affiche des messages d'erreur si le fichier n'existe pas ou si
            l'encodage est incorrect.
        """
        sets = {}
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)

                for i in reader:
                    if len(i) < 4:  # Si la ligne n'a pas assez de colonnes
                        continue

                    title, question, answer, set_name = i[0], i[1], i[2], i[3]

                    if set_name not in sets:  # Si le set n'existe pas encore
                        sets[set_name] = Group(set_name)

                    sets[set_name].add_flashcard(
                        Flashcard(title, question, answer))

            return sets

        except FileNotFoundError:  # fichier pas trouvé
            UI.show_error_popup('FileNotFoundError', "Le fichier n'a pas " +
                                "été trouvé à l'emplacement spécifié.")
            return sets

        except UnicodeDecodeError:  # Si mauvais encodage
            UI.show_error_popup('UnicodeDecodeError',
                                "Erreur de décodage du fichier avec " +
                                "l'encodage UTF-8."
                                "Vérifie l'encodage."
                                )

        return sets  # si on n'a pas pu lire ça, renvoie les sets vides

    def create_flashcard(self, title: str, question: str,
                         answer: str, set_name: str):
        """    #Thomas
        @description:
            Crée une nouvelle flashcard et l'ajoute au set désigné, en
            l'enregistrant dans un fichier CSV.
        @pre:
            * `title`, `question`, `answer`, et `set_name` sont des chaînes
            non vides.
        @post:
            * La flashcard est ajoutée au set et enregistrée dans `listes.csv`.
            * Affiche un message d'erreur si l'écriture dans le fichier
            CSV échoue.
        """
        if set_name not in self.sets:  # Vérif si le set existe sinn on le crée
            self.sets[set_name] = Group(set_name)

        new_card = Flashcard(title, question, answer)   # créer la carte
        self.sets[set_name].add_flashcard(new_card)
        print(
            "Flashcard '" + title + "' ajoutée dans le set '" + set_name + "'."
        )

        # Ajoute la flashcard au fichier CSV
        try:
            with open(
                "listes.csv", mode='a', encoding='utf-8', newline=''
            ) as file:
                writer = csv.writer(file)
                writer.writerow([title, question, answer, set_name])
        except Exception as e:
            UI.show_error_popup('Exception',
                                "Erreur lors de l'écriture " +
                                f"dans le fichier CSV : {e}")

    def display_statistics(self):
        """     #Mathéo
        @description:
            Affiche les statistiques de chaques cartes.

        @pre:
            * récupère la carte affichée.
        @post:
            * renvoie les statistique propre a la carte.
        """
        pass

    def display_badge(self):
        pass

    def send_reminder(self, reminder_date: date,
                      reminder_time: time, cards_to_review: List[Flashcard]):
        """     #Mathéo
        @description:
            Envoie les données a la classe reminder.
        @pre:
            * 'reminder_date' est un champ date, 'reminder_time' est un champ
            time, 'cards_to_review' est une liste des cartes a réviser.
        @post:
            * Une liste des donnée reçus en paramètre.
        """
        pass

    def switch_revision_mode(mode: str):
        pass


class UI:
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        """     #Mathéo
        @description:
            Instance la fenêtre de l'application et dispose les élément.
        @pre:
            * Aucune prédisposition.
        @post:
            * La fenêtre est créée.
        """
        # Initialisation de l'interface utilisateur
        self.window.title('FlashCards')
        # self.window.geometry('1920x1080')
        self.window.state('zoomed')
        self.window.minsize(600, 900)
        # self.window.iconbitmap('images/logobidon.ico')
        self.window.config(background='#f5f5f5')

        # Frame pour le titre
        self.titleFrame = Frame(self.window, bg='#f5f5f5')
        self.titleFrame.pack(expand=True, anchor='center')

        # Menu
        self.menubar = Menu(self.window)
        self.settingsmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Settings", menu=self.settingsmenu)
        self.settingsmenu.add_command(
            label='Dark Theme', command=self.toggle_mode
        )
        self.settingsmenu.add_separator()
        self.settingsmenu.add_command(
            label='Fermer Application', command=self.on_closing
        )
        self.window.config(menu=self.menubar)

        # Label Titre
        self.label_title = Label(
            self.titleFrame, text='Bienvenue Mr Jean-Révise',
            font=('Helvetica', 30), bg="#f5f5f5", fg='black'
        )
        self.label_title.pack()

        # Frame principale
        self.frame = Frame(self.window, bg='#f5f5f5')
        self.frame.pack(expand=True, fill='both', anchor='center')

        # Frame pour les badges, en haut a droite
        self.badge_frame = Frame(
            self.frame, bg='#e5884b', width=200, height=100
        )
        self.badge_frame.place(relx=0.98, rely=0.0, anchor='ne')  # haut droite

        # Label badges
        self.badge_label = Label(
            self.badge_frame, text=self.app.stats.send_badges(),
            font=('Helvetica', 12), bg='#e5884b', fg='white'
        )
        self.badge_label.pack(pady=10, padx=10)  # Ajout de marges

        # Choix de set
        self.set_choice = StringVar(self.frame)
        self.set_choice.set("Choisir un groupe")
        self.set_menu = ttk.Combobox(
            self.frame, textvariable=self.set_choice,
            values=list(self.app.sets.keys())
        )
        self.set_menu.pack(pady=10)
        self.set_menu.config(width=20)

        # Canvas
        self.canvas = Canvas(self.frame, width=400, height=300, bg='#f5ebe0')
        self.canvas.pack(pady=20, expand=True)

        # Bouton commencer
        self.start_button = Button(
            self.frame, text="Commencer la révision",
            command=self.start_revision, bg='#468faf', fg='white'
        )
        self.start_button.pack(pady=5)

        # Label pour la question
        self.question_label = Label(
            self.frame, text="", font=('Courier New', 20),
            bg="#f5f5f5", fg="black"
        )
        self.question_label.pack()

        # Frame pour les boutons de réponse
        self.button_frame = Frame(self.frame, bg="#f5f5f5")
        self.button_frame.pack(pady=20, anchor='center')

        # Boutons pour réponses
        self.answer_button = Button(
            self.button_frame, text="Montrer la réponse",
            command=None, bg='#adb5bd'
        )
        self.answer_button.grid(row=0, column=1, padx=5, pady=1)

        self.correct_button = Button(
            self.button_frame, text="Correct",
            command=None, bg='#55a630'
        )
        self.correct_button.grid(row=0, column=0, padx=5, pady=5)

        self.incorrect_button = Button(
            self.button_frame, text="Incorrect",
            command=None, bg='#e71d36'
            )
        self.incorrect_button.grid(row=0, column=2, padx=5, pady=5)

        # Statistiques
        self.stats_label = Label(
            self.frame, text=self.app.stats.send_stats(),
            font=('Courier New', 12), bg="#f5f5f5", fg="black"
        )
        self.stats_label.pack()

        # Frame pour ajouter une flashcard
        self.add_card_frame = Frame(self.frame, bg="#f5f5f5")
        self.add_card_frame.pack(pady=10, anchor='center')

        # Entrées pour les flashcards
        self.question_entry_label = Label(
            self.add_card_frame, text="Question:",
            font=('Courier New', 12), bg="#f5f5f5"
        )
        self.question_entry_label.grid(row=0, column=0, padx=5, pady=5)
        self.question_entry = Entry(
            self.add_card_frame,
            font=('Courier New', 12), width=30
        )
        self.question_entry.grid(row=0, column=1, padx=5, pady=5)

        self.answer_entry_label = Label(
            self.add_card_frame, text="Réponse:",
            font=('Courier New', 12), bg="#f5f5f5"
        )
        self.answer_entry_label.grid(row=1, column=0, padx=5, pady=5)
        self.answer_entry = Entry(
            self.add_card_frame,
            font=('Courier New', 12), width=30
        )
        self.answer_entry.grid(row=1, column=1, padx=5, pady=5)

        self.title_entry_label = Label(
            self.add_card_frame, text="Titre:",
            font=('Courier New', 12), bg="#f5f5f5"
        )
        self.title_entry_label.grid(row=2, column=0, padx=5, pady=5)
        self.title_entry = Entry(
            self.add_card_frame,
            font=('Courier New', 12), width=30
        )
        self.title_entry.grid(row=2, column=1, padx=5, pady=5)

        self.set_entry_label = Label(
            self.add_card_frame, text="Set:",
            font=('Courier New', 12), bg="#f5f5f5"
        )
        self.set_entry_label.grid(row=3, column=0, padx=5, pady=5)
        self.set_entry = Entry(
            self.add_card_frame,
            font=('Courier New', 12), width=30
        )
        self.set_entry.grid(row=3, column=1, padx=5, pady=5)

        # Bouton Ajouter une flashcard
        self.add_button = Button(
            self.add_card_frame, text="Ajouter une flashcard",
            command=self.add_flashcard, bg='#f6aa1c'
        )
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Fermer l'application proprement
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_error_popup(title: str, message: str):
        """ Affiche un pop-up , pour les msg d'erreur """
        messagebox.showerror(title, message)

    def on_closing(self):
        if messagebox.askyesno(
            title="Fermer ?", message="Vous voulez vraiment fermer l'app ?"
        ):
            self.window.destroy()

    def toggle_mode(self):
        """     #Mathéo
        @description:
            Switch entre les deux mode d'affichage.
        @pre:
            * Aucune prédisposition
        @post:
            * Change l'affichage entre le Dark mode et Light mode
        """
        if self.window.cget('bg') == '#f5f5f5':
            # Mode sombre
            self.window.config(background='black')
            self.titleFrame.config(background='black')
            self.frame.config(background='#000')
            self.label_title.config(bg='black', fg='white')
            self.set_menu.config(background='gray', foreground='black')
            self.canvas.config(bg='black')
            self.start_button.config(bg='darkgray', fg='white')
            self.question_label.config(bg='black', fg='white')
            self.button_frame.config(bg='black')
            self.answer_button.config(bg='darkgray', fg='white')
            self.correct_button.config(bg='darkgreen', fg='white')
            self.incorrect_button.config(bg='darkred', fg='white')
            self.stats_label.config(bg='black', fg='white')
            self.add_card_frame.config(bg='black')
            self.question_entry_label.config(bg='black', fg='white')
            self.answer_entry_label.config(bg='black', fg='white')
            self.title_entry_label.config(bg='black', fg='white')
            self.set_entry_label.config(bg='black', fg='white')
            self.question_entry.config(bg='gray', fg='white')
            self.answer_entry.config(bg='gray', fg='white')
            self.title_entry.config(bg='gray', fg='white')
            self.set_entry.config(bg='gray', fg='white')
            self.add_button.config(bg='darkorange', fg='white')

            if not self.set_menu.get():
                self.set_menu.set('Choisir un set')

        else:
            # Mode clair
            self.window.config(background='#f5f5f5')
            self.titleFrame.config(background='#f5f5f5')
            self.frame.config(background='#f5f5f5')
            self.label_title.config(bg='#f5f5f5', fg='black')
            self.set_menu.config(background='#f5f5f5', foreground='black')
            self.canvas.config(bg='#f5ebe0')
            self.start_button.config(bg='blue', fg='#f5f5f5')
            self.question_label.config(bg='#f5f5f5', fg='black')
            self.button_frame.config(bg='#f5f5f5')
            self.answer_button.config(bg='#adb5bd', fg='black')
            self.correct_button.config(bg='#55a630', fg='black')
            self.incorrect_button.config(bg='#e71d36', fg='black')
            self.stats_label.config(bg='#f5f5f5', fg='black')
            self.add_card_frame.config(bg='#f5f5f5')
            self.question_entry_label.config(bg='#f5f5f5', fg='black')
            self.answer_entry_label.config(bg='#f5f5f5', fg='black')
            self.title_entry_label.config(bg='#f5f5f5', fg='black')
            self.set_entry_label.config(bg='#f5f5f5', fg='black')
            self.question_entry.config(bg='#f5f5f5', fg='black')
            self.answer_entry.config(bg='#f5f5f5', fg='black')
            self.title_entry.config(bg='#f5f5f5', fg='black')
            self.set_entry.config(bg='#f5f5f5', fg='black')
            self.add_button.config(bg='#f6aa1c', fg='black')

            if not self.set_menu.get():
                self.set_menu.set('Choisir un set')

    def start_revision(self):
        """ #Nathan
        @description:
        Démarre la révision pour un set sélectionné
        @pré:
        * self.set_choice contient le nom du set sélectionné dans
        le menu déroulant
        * self.app.sets est un dictionnaire contenant des ensembles de cartes
        @post:
        * Si un set valide avec des cartes est sélectionné, une carte
        aléatoire de cet ensemble est affichée en appelant show_card
        * Si le set est vide ou non trouvé, un message indiquant qu'aucune
        carte n'est disponible est affiché
        """

        selected_set_name = self.set_choice.get()
        current_set = self.app.sets.get(selected_set_name)
        if current_set and current_set.cards:
            current_card = random.choice(current_set.cards)
            self.show_card(current_card)
        else:
            self.question_label.config(
                text="Aucune carte disponible dans ce set."
            )

    def show_card(self, card):
        """ #Nathan
            @description:
            Affiche la question lié à une carte sur le canevas

            @pré:
            * card est une instance de Flashcard contenant une question et
            une réponse

            @post:
            * Le canevas est mis à jour pour afficher la question de la carte
            * Le bouton pour afficher la réponse est configuré pour appeler
            show_answer avec la carte actuelle
        """
        self.canvas.delete("all")
        self.draw_card(self.canvas, card, 50, 50, 300, 200)
        self.answer_button.config(command=lambda: self.show_answer(card))

    def show_answer(self, card):
        """ #Nathan
        Affiche la réponse de la carte et configure les boutons d'évaluation

        @pré:
        * card est une instance de Flashcard contenant une réponse à afficher

        @post:
        * Le canevas est mis à jour pour afficher la réponse de la carte
        * Les boutons d'évaluation ("Correct" et "Incorrect") sont configurés
        pour appeler la méthode evaluate avec la réponse correcte ou incorrecte
    """
        self.canvas.delete("all")
        self.draw_card(self.canvas, card, 50, 50, 300, 200, answer=True)
        self.correct_button.config(command=lambda: self.evaluate(card, True))
        self.incorrect_button.config(
            command=lambda: self.evaluate(card, False)
        )

    def evaluate(self, card, correct):
        """ #Nathan
        @description:
        Evalue la réponse de l'utilisateur et met à jour les statistiques

        @pré:
        * card est une instance de Flashcard qui sera mise à jour en fonction
        de la réponse (correct ou incorrect)
        * correct est un booléen indiquant si la réponse donnée par
        l'utilisateur est correcte

        @post:
        * La carte est mise à jour en utilisant la méthode review pour ajuster
        son niveau de révision
        * Les statistiques de l'application sont mises à jour avec
        calculate_progress
        * Le label des statistiques affiche les statistiques mises à jour
        * La révision reprend avec start_revision
        """
        card.review(correct)
        self.app.stats.calculate_progress(correct)
        self.stats_label.config(text=self.app.stats.send_stats())
        self.badge_label.config(text=self.app.stats.send_badges())
        self.start_revision()

    def update_set_menu(self):
        """ #Nathan
        @description:
        Met à jour le menu déroulant des ensembles disponibles

        @pré:
        * self.app.sets contient les ensembles actuellement chargés dans
        l'application

        @post:
        * Le menu déroulant set_menu est mis à jour avec les noms des
        ensembles disponibles
        * Si aucun ensemble n'est sélectionné, le menu est défini par
        défaut sur "Choisir un set"
        """
        self.set_menu['values'] = list(self.app.sets.keys())
        if not self.set_menu.get():
            self.set_menu.set('Choisir un set')

    def draw_card(self, canvas, card, x, y, width, height, answer=False):
        """     #Mathéo
        @description :
            Affiche la carte de révison sur le canvas a un emplacement donné
            en paramètre ('x', 'y').
            Si 'answer' est True la réponse est affichée sur la carte sinon la
            question est affichée.

        @pré:
            * 'canvas' est un objet Canvas de Tkinter,
            * 'card' est un objet ayant pour attributs 'question' et 'answer',
            elle contient les textes de la question et de la réponse,
            * 'x' et 'y' sont des int qui représentent les coordonnées de
            l'origine de la carte,
            * 'width' et 'height' sont des int qui représentent la largeur et
            la hauteur de la carte.

        @post:
            * Une carte de largeur et hauteur spécifié est créée sur le canvas,
            la question ou la réponse sont inscrit au centre de celle-ci.
        """
        canvas.create_rectangle(
            x, y, x + width, y + height, fill='lightblue', outline='black'
        )
        if answer:
            text = f"Réponse: {card.answer}"
        else:
            text = card.question

        canvas.create_text(
            x + width / 2, y + height / 2, text=text,
            font=('Courier New', 16), fill='black'
        )

    def add_flashcard(self):
        """     #Mathéo
        @description :
            Ajoute une nouvelle carte en incluant la question, la réponse, le
            titre et le nom du set.
            Met à jours les sets disponibles et vides les champs de saisie
            après l'ajout d'une carte.

        @pré:
            * 'question', 'answer' et 'title' sont des strings non vides.

        @post:
            * Une nouvelle carte est ajoutée à l'application,
            * Les sets disponible sont mit à jours et les champs de saisie
            sont vidés.
        """
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

        else:
            UI.show_error_popup('NotEnoughArguments',
                                'Veuillez remplir toutes les cases')


# Créer une instance de l'application
app = Application(app_name='FlashCards', version='1.0')

# Créer fenêtre
window = Tk()

# Créer une instance de l'interface utilisateur
ui = UI(window, app)

# Lancer la fenêtre
window.mainloop()
