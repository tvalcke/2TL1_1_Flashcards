import unittest
from app import Flashcard
from app import Group
from app import Statistics

class unittest_matheo(unittest.TestCase):

    def setUp(self):
        self.group = Group(name="Math")
        self.flashcard = Flashcard(
            title="Test Title",
            question="What is 2 + 2?",
            answer="4"
        )
        self.stats = Statistics()

    def test_stats_userxp(self):
        self.assertEqual(self.stats.user_xp, 0)         #Vérif initiation à 0

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.user_xp, 100)       #Vérif incrémentation de l'expérience

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.user_xp, 210)       #Vérif incrémentation de l'expérience

        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.user_xp, 210)       #Vérif non-incrémentation de l'expérience

        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.user_xp, 210)       #Vérif non-incrémentation de l'expérience après 2 réponse fausse consécutive

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.user_xp, 310)       #Vérif incrémentation de l'expérience après une réponse fausse

    def test_stats_cards_reviewed(self):
        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.cards_reviewed, 1)  #Vérif incrémentation du nombre de cartes vue

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.cards_reviewed, 2)  #Vérif incrémentation du nombre de cartes vue

        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.cards_reviewed, 3)  #Vérif incrémentation du nombre de cartes vue

        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.cards_reviewed, 4)  #Vérif incrémentation du nombre de cartes vue

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.cards_reviewed, 5)  #Vérif incrémentation du nombre de cartes vue

    def test_stats_streak_count(self):
        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.streak_count, 0.1)  #Vérif incrémentation streak_count

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.streak_count, 0.2)  #Vérif incrémentation streak_count

        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.streak_count, 0)    #Vérif reset streak_count

        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.streak_count, 0)    #Vérif reset streak_count

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.streak_count, 0.1)  #Vérif incrémentation streak_count

    def test_stats_correct_answer(self):
        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.correct_answers, 1) #Vérif incrémentation réponse correct

        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.correct_answers, 2) #Vérif incrémentation réponse correct
        
        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.correct_answers, 2) #Vérif non-incrémentation réponse correct
        
        self.stats.calculate_progress(correct=False)    #Simulation d'une réponse fausse
        self.assertEqual(self.stats.correct_answers, 2) #Vérif non-incrémentation réponse correct
        
        self.stats.calculate_progress(correct=True)     #Simulation d'une réponse correct
        self.assertEqual(self.stats.correct_answers, 3) #Vérif incrémentation réponse correct

    def test_stats_send_stats(self):
        self.stats.calculate_progress(correct=True)                                                                         #Simulation d'une réponse correct
        self.assertEqual(self.stats.send_stats(), "Nombre de cartes vues: 1, précision: 100.0 %. \n\nXP: 100 Combo :1")     #Vérif String stat    

        self.stats.calculate_progress(correct=True)                                                                         #Simulation d'une réponse correct
        self.assertEqual(self.stats.send_stats(), "Nombre de cartes vues: 2, précision: 100.0 %. \n\nXP: 210 Combo :2")     #Vérif String stat

        self.stats.calculate_progress(correct=False)                                                                        #Simulation d'une réponse fausse
        self.assertEqual(self.stats.send_stats(), "Nombre de cartes vues: 3, précision: 66.67 %. \n\nXP: 210 Combo :0")     #Vérif String stat

        self.stats.calculate_progress(correct=False)                                                                        #Simulation d'une réponse fausse
        self.assertEqual(self.stats.send_stats(), "Nombre de cartes vues: 4, précision: 50.0 %. \n\nXP: 210 Combo :0")      #Vérif String stat
        
        self.stats.calculate_progress(correct=True)                                                                         #Simulation d'une réponse correct
        self.assertEqual(self.stats.send_stats(), "Nombre de cartes vues: 5, précision: 60.0 %. \n\nXP: 310 Combo :1")      #Vérif String stat


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
