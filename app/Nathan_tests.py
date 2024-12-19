import unittest
from datetime import datetime, timedelta
from app import Flashcard, Group, Statistics, Application, Badge

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

    def test_add_invalid_flashcard(self):
        group = Group("Math")
        with self.assertRaises(TypeError):
            group.add_flashcard("Not a Flashcard")

class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.stats = Statistics()

    def test_calculate_xp_correct(self):
        self.stats.calculate_Xp(True)
        self.assertEqual(self.stats.user_xp, 100)
        self.assertEqual(self.stats.streak_count, 0.1)

    def test_calculate_xp_incorrect(self):
        self.stats.calculate_Xp(False)
        self.assertEqual(self.stats.streak_count, 0.0)

    def test_unlock_badge(self):
        self.stats.user_xp = 250
        self.stats.unlock_badge()
        badge_names = [badge.name for badge in self.stats.badges if badge.earned]
        self.assertIn("Intermédiaire", badge_names)

    def test_send_stats(self):
        self.stats.cards_reviewed = 10
        self.stats.correct_answers = 8
        result = self.stats.send_stats()
        self.assertIn("précision: 80.0 %", result)

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application("TestApp", "1.0")
        self.test_set_name = "Test Set"
        self.test_flashcard = Flashcard(
            title="Capital of France",
            question="What is the capital of France?",
            answer="Paris"
        )
        self.app.sets[self.test_set_name] = Group(self.test_set_name)
        self.app.sets[self.test_set_name].add_flashcard(self.test_flashcard)

    def test_import_flashcards_from_csv(self):
        imported_sets = self.app.import_flashcards_from_csv("listes.csv")
        self.assertIsInstance(imported_sets, dict)
        for set_name, group in imported_sets.items():
            self.assertIsInstance(group, Group)
            for flashcard in group.cards:
                self.assertIsInstance(flashcard, Flashcard)

    def test_create_flashcard(self):
        initial_count = len(self.app.sets[self.test_set_name].cards)
        self.app.create_flashcard(
            title="Capital of Spain",
            question="What is the capital of Spain?",
            answer="Madrid",
            set_name=self.test_set_name
        )
        self.assertEqual(len(self.app.sets[self.test_set_name].cards), initial_count + 1)
        new_card = self.app.sets[self.test_set_name].cards[-1]
        self.assertEqual(new_card.title, "Capital of Spain")
        self.assertEqual(new_card.question, "What is the capital of Spain?")
        self.assertEqual(new_card.answer, "Madrid")

    def test_statistics_integration(self):
        self.assertEqual(self.app.stats.cards_reviewed, 0)
        self.app.stats.calculate_progress(correct=True)
        self.assertEqual(self.app.stats.cards_reviewed, 1)
        self.assertEqual(self.app.stats.correct_answers, 1)

    def test_delete_flashcard(self):
        initial_count = len(self.app.sets[self.test_set_name].cards)
        card_to_delete = self.app.sets[self.test_set_name].cards[0]
        self.app.sets[self.test_set_name].cards.remove(card_to_delete)
        self.assertEqual(len(self.app.sets[self.test_set_name].cards), initial_count - 1)

    def test_update_flashcard(self):
        card_to_update = self.app.sets[self.test_set_name].cards[0]
        card_to_update.question = "Updated Question"
        self.assertEqual(card_to_update.question, "Updated Question")

    def test_list_all_sets(self):
        sets_list = list(self.app.sets.keys())
        self.assertIn(self.test_set_name, sets_list)
        self.assertIsInstance(sets_list, list)

    def test_empty_set_handling(self):
        empty_set_name = "Empty Set"
        self.app.sets[empty_set_name] = Group(empty_set_name)
        self.assertEqual(len(self.app.sets[empty_set_name].cards), 0)

class TestBadge(unittest.TestCase):
    def test_check_criteria(self):
        badge = Badge("Test Badge", "Earn 100 XP", 100)
        self.assertTrue(badge.check_criteria(100))
        self.assertFalse(badge.check_criteria(50))

    def test_assign_badge(self):
        badge = Badge("Test Badge", "Earn 100 XP", 100)
        badge.assign_badge()
        self.assertTrue(badge.earned)
        self.assertIsNotNone(badge.date_earned)


class test_statistique(unittest.TestCase):

    def setUp(self):
        self.group = Group(name="Math")
        self.flashcard = Flashcard(
            title="Test Title",
            question="What is 2 + 2?",
            answer="4"
        )
        self.stats = Statistics()

    def test_stats_userxp(self):
        self.assertEqual(self.stats.user_xp, 0)         

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.user_xp, 100)       

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.user_xp, 210)      

        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.user_xp, 210)       

        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.user_xp, 210)       

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.user_xp, 310)       

    def test_stats_cards_reviewed(self):
        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.cards_reviewed, 1)  

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.cards_reviewed, 2)  

        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.cards_reviewed, 3)  

        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.cards_reviewed, 4)

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.cards_reviewed, 5)  

    def test_stats_streak_count(self):
        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.streak_count, 0.1) 

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.streak_count, 0.2)  

        self.stats.calculate_progress(correct=False)  
        self.assertEqual(self.stats.streak_count, 0)    

        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.streak_count, 0)    

        self.stats.calculate_progress(correct=True)    
        self.assertEqual(self.stats.streak_count, 0.1)  

    def test_stats_correct_answer(self):
        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.correct_answers, 1) 

        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.correct_answers, 2) 
        
        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.correct_answers, 2) 
        
        self.stats.calculate_progress(correct=False)    
        self.assertEqual(self.stats.correct_answers, 2)
        
        self.stats.calculate_progress(correct=True)     
        self.assertEqual(self.stats.correct_answers, 3) 


if __name__ == "__main__":
    unittest.main()
