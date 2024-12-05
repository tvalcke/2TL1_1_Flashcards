import unittest
from datetime import datetime, timedelta
from app import Flashcard
from app import Group
from app import Statistics 
from app import Application


### Test unitaire Nathan ###
### Faits à l'aide de chatGPT ###

class TestFlashcard(unittest.TestCase):
    def test_review_correct(self):
        card = Flashcard("Title", "What is 2+2?", "4")
        card.review(True)  # Bonne réponse
        self.assertEqual(card.review_level, 1)
        self.assertAlmostEqual(
            card.next_review_date,
            datetime.now() + timedelta(days=2),
            delta=timedelta(seconds=1)
        )

    def test_review_incorrect(self):
        card = Flashcard("Title", "What is 2+2?", "4", review_level=2)
        card.review(False)  # Mauvaise réponse
        self.assertEqual(card.review_level, 1)
        self.assertAlmostEqual(
            card.next_review_date,
            datetime.now() + timedelta(days=2),
            delta=timedelta(seconds=1)
        )


class TestGroup(unittest.TestCase):
    def test_add_flashcard(self):
        group = Group("Math")
        card = Flashcard("Addition", "What is 2+2?", "4")
        group.add_flashcard(card)
        self.assertIn(card, group.cards)


class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.stats = Statistics()

    def test_send_stats(self):
        self.stats.cards_reviewed = 10
        self.stats.correct_answers = 8
        result = self.stats.send_stats()
        self.assertIn("précision: 80.0 %", result)


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application("TestApp", "1.0")

    def test_import_flashcards_from_csv(self):
        sets = self.app.import_flashcards_from_csv("listes.csv")
        self.assertIsInstance(sets, dict)


class TestApplication(unittest.TestCase):
    def setUp(self):
        """Initialise une instance d'Application avant chaque test."""
        self.app = Application("Flashcard App", "1.0")
        self.test_set_name = "Test Set"
        self.test_flashcard = Flashcard(
            title="Capital of France",
            question="What is the capital of France?",
            answer="Paris"
        )
        # Ajouter un ensemble de test et une carte associée
        self.app.sets[self.test_set_name] = Group(self.test_set_name)
        self.app.sets[self.test_set_name].add_flashcard(self.test_flashcard)

    def test_import_flashcards_from_csv(self):
        """Test de l'importation des flashcards depuis un fichier CSV."""
        imported_sets = self.app.import_flashcards_from_csv("listes.csv")
        self.assertIsInstance(imported_sets, dict)
        # Assurez-vous qu'il y a des sets ou qu'ils sont bien formatés
        for set_name, group in imported_sets.items():
            self.assertIsInstance(group, Group)
            for flashcard in group.cards:
                self.assertIsInstance(flashcard, Flashcard)

    def test_create_flashcard(self):
        """Test de création de flashcards et ajout au fichier CSV."""
        initial_count = len(self.app.sets[self.test_set_name].cards)
        self.app.create_flashcard(
            title="Capital of Spain",
            question="What is the capital of Spain?",
            answer="Madrid",
            set_name=self.test_set_name
        )
        # Vérifie que le nombre de cartes dans l'ensemble a augmenté
        self.assertEqual(len(self.app.sets[self.test_set_name].cards), initial_count + 1)
        # Vérifie que la nouvelle carte a les bonnes informations
        new_card = self.app.sets[self.test_set_name].cards[-1]
        self.assertEqual(new_card.title, "Capital of Spain")
        self.assertEqual(new_card.question, "What is the capital of Spain?")
        self.assertEqual(new_card.answer, "Madrid")

    def test_display_statistics(self):
        """Test de l'affichage des statistiques (stubbed)."""
        # Stub simple pour vérifier que la méthode est callable
        self.assertIsNone(self.app.display_statistics())


    def test_statistics_class_integration(self):
        """Test de l'intégration avec la classe Statistics."""
        self.assertEqual(self.app.stats.cards_reviewed, 0)
        self.app.stats.calculate_progress(correct=True)
        self.assertEqual(self.app.stats.cards_reviewed, 1)
        self.assertEqual(self.app.stats.correct_answers, 1)



if __name__ == "__main__":
    unittest.main()
