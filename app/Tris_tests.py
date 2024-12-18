import unittest
from app import Flashcard
from app import Group

# ######## tests unitaires Tris #########
# mes tests unitaires on été partiellement écrits avec l'aide de Mistral.ai


class TestsTristan(unittest.TestCase):

    def setUp(self):  # setup une flashcard pour faire les tests
        """Initialisation d'un groupe et d'une flashcard avant chaque test"""
        self.group = Group(name="Math")
        self.flashcard = Flashcard(
            title="Test Title",
            question="What is 2 + 2?",
            answer="4"
        )

    # tests unitaires pour la méthode 'review' dans la class Flashacrd

    def test_review_correct_answer_increases_review_level(self):
        """vérifie  le niveau de révision augmente
        quand la réponse est correcte"""
        initial_review_level = self.flashcard.review_level
        self.flashcard.review(correct=True)

        self.assertEqual(
            self.flashcard.review_level, initial_review_level + 1
        )

    def test_review_level_increases_properly(self):
        """Test que le niveau de révision augmente correctement
        après plusieurs réponses correctes"""
        self.flashcard.review_level = 2  # On commence avec un niveau 2
        initial_review_level = self.flashcard.review_level

        # Effectuer plusieurs révisions correctes
        self.flashcard.review(correct=True)
        self.flashcard.review(correct=True)

        # Vérification que le niveau de révision a bien augmenté
        self.assertEqual(self.flashcard.review_level, initial_review_level + 2)

    def test_review_incorrect_answer_decreases_review_level(self):
        """Test que le niveau de révision diminue
        quand la réponse est incorrecte"""
        self.flashcard.review_level = 2  # On commence avec un niveau 2
        initial_review_level = self.flashcard.review_level
        self.flashcard.review(correct=False)

        self.assertEqual(
            self.flashcard.review_level, initial_review_level - 1
        )

    def test_review_level_does_not_increase_on_invalid_review(self):
        """Test que le niveau de révision
        n'augmente pas de manière inattendue"""
        self.flashcard.review_level = 0  # On commence avec un niveau 0
        initial_review_level = self.flashcard.review_level

        # Simuler une réponse correcte puis une réponse incorrecte
        self.flashcard.review(correct=True)
        self.flashcard.review(correct=False)

        # Vérification que le niveau de révision reste correct
        self.assertEqual(self.flashcard.review_level, initial_review_level)

    def test_review_level_does_not_go_below_zero(self):
        """Test que le niveau de révision ne devient pas inférieur à zéro"""
        self.flashcard.review_level = 0  # On commence avec un niveau 0
        self.flashcard.review(correct=False)

        self.assertEqual(self.flashcard.review_level, 0)

    def test_next_review_date_increases_after_correct_answer(self):
        """Test que la date de la prochaine révision est mise à jour
        après une réponse correcte"""
        initial_next_review_date = self.flashcard.next_review_date
        self.flashcard.review(correct=True)

        # Vérification que la prochaine révision est après la date initiale,
        # en fonction du niveau de révision
        self.assertGreater(
            self.flashcard.next_review_date, initial_next_review_date
        )

    def test_next_review_date_changes_after_incorrect_answer(self):
        """Test que la date de la prochaine révision est mise à jour
        après une réponse incorrecte"""
        self.flashcard.review_level = 2  # On commence avec un niveau 2
        initial_next_review_date = self.flashcard.next_review_date
        self.flashcard.review(correct=False)

        # Vérification que la prochaine révision est après la date initiale,
        # en fonction du niveau de révision
        self.assertGreater(
            self.flashcard.next_review_date, initial_next_review_date
        )

    def test_next_review_date_correct_is_after_incorrect(self):
        """Test que la date de la prochaine révision après une réponse correcte
        est postérieure à celle d'une réponse incorrecte"""

        # On initialise les dates avant les réponses
        initial_next_review_date_incorrect = self.flashcard.next_review_date
        self.flashcard.review(correct=False)  # Réponse incorrecte
        next_review_after_incorrect = self.flashcard.next_review_date

        # On réinitialise le niveau et la date pour la réponse correcte
        self.flashcard.next_review_date = initial_next_review_date_incorrect
        self.flashcard.review_level = 0  # Remise à zéro du niveau de révision

        # Réponse correcte
        self.flashcard.review(correct=True)
        next_review_after_correct = self.flashcard.next_review_date

        # Vérification que la date après la réponse correcte est bien après
        # celle après la réponse incorrecte
        self.assertGreater(
            next_review_after_correct, next_review_after_incorrect
        )

    def test_review_overflow_error(self):
        """Test qu'un OverflowError est levé si le niveau de
        révision est trop élevé"""
        # On fixe un niveau de révision très élevé
        self.flashcard.review_level = 1000  # nv max

        with self.assertRaises(ValueError) as context:
            self.flashcard.review(correct=True)

        self.assertTrue(
            "Review level trop élevé pour être calculé"
            in str(context.exception))

    # tests unitaires pour la méthode 'add_flashcard'
    # dans la class Group

    def test_add_flashcard_to_empty_group(self):
        """Vérifie que l'ajout d'une flashcard à un groupe vide fonctionne
        donc que le grp se crée"""
        initial_card_count = len(self.group.cards)
        self.group.add_flashcard(self.flashcard)

        self.assertEqual(len(self.group.cards), initial_card_count + 1)
        self.assertIn(self.flashcard, self.group.cards)

    def test_add_multiple_flashcards(self):
        """Vérifie que l'ajout de plusieurs flashcards fonctionne
        correctement"""
        flashcard_2 = Flashcard(
            title="Test Title 2",
            question="What is 3 + 3?",
            answer="6"
        )
        self.group.add_flashcard(self.flashcard)
        self.group.add_flashcard(flashcard_2)

        self.assertEqual(len(self.group.cards), 2)
        self.assertIn(self.flashcard, self.group.cards)
        self.assertIn(flashcard_2, self.group.cards)

    def test_add_flashcard_to_group_with_existing_cards(self):
        """Vérifie que l'ajout d'une flashcard à un groupe déjà
        rempli fonctionne"""
        flashcard_2 = Flashcard(
            title="Test Title 2",
            question="What is 3 + 3?",
            answer="6"
        )
        self.group.add_flashcard(self.flashcard)
        initial_card_count = len(self.group.cards)

        self.group.add_flashcard(flashcard_2)

        self.assertEqual(len(self.group.cards), initial_card_count + 1)
        self.assertIn(flashcard_2, self.group.cards)

    def test_flashcard_is_added_correctly(self):
        """Vérifie que la flashcard ajoutée contient les bonnes informations"""
        self.group.add_flashcard(self.flashcard)

        added_flashcard = self.group.cards[0]
        self.assertEqual(added_flashcard.title, "Test Title")
        self.assertEqual(added_flashcard.question, "What is 2 + 2?")
        self.assertEqual(added_flashcard.answer, "4")

    def test_add_flashcard_with_invalid_type(self):
        """Vérifie que l'ajout d'un objet non valide"
        " (pas une instance de Flashcard) soulève une exception"""
        with self.assertRaises(TypeError):
            # Passer une chaîne de caractères au lieu
            # d'une instance de Flashcard
            self.group.add_flashcard("Invalid Flashcard")
        with self.assertRaises(TypeError):
            self.group.add_flashcard(58)


if __name__ == "__main__":
    unittest.main()

"""
    Les tests que j'ai écrit n'ont pas réussi du premier coup, j'ai eu quelques
erreurs au niveau des exeptions que je ne gérait pas bien ou pas du tout.
J'ai du adapter le code et mes tests en fonction de ces erreurs.

    Comme dans le tp9, j'ai également du revoir certaines préconditions et les
élargir pour les exeptions que j'ai rajouté ou que j'ai testé

    J'a également choisit de ne pas mettre toutes les exeptions pour pouvoir
justement laisser ces conditions dans les pré de la méthode concernée

    Le code coverage des tests effectués est de 99% selon le module coverage
sur Visual Studio code
"""
