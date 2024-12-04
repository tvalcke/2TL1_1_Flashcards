import unittest
from datetime import datetime
from app import Badge

"Tests réalisés avec l'aide de chatgpt"

class unittest_badge(unittest.TestCase):

    def setUp(self):
        self.badge_beginner = Badge(
            name="Beginner",
            description="Earned for reaching 100 XP",
            xp_threshold=100
        )
        self.badge_intermediate = Badge(
            name="Intermediate",
            description="Earned for reaching 500 XP",
            xp_threshold=500
        )

    def test_check_criteria(self):
        # Vérif badge non débloqué si XP inférieur au seuil
        self.assertFalse(self.badge_beginner.check_criteria(user_xp=50))

        # Vérif badge débloqué si XP égal au seuil
        self.assertTrue(self.badge_beginner.check_criteria(user_xp=100))

        # Vérif badge débloqué si XP supérieur au seuil
        self.assertTrue(self.badge_beginner.check_criteria(user_xp=150))

        # Vérif badge non redébloqué après obtention
        self.badge_beginner.earned = True
        self.assertFalse(self.badge_beginner.check_criteria(user_xp=200))

    def test_assign_badge(self):
        # Vérif état initial du badge
        self.assertFalse(self.badge_beginner.earned)
        self.assertIsNone(self.badge_beginner.date_earned)

        # Attribution du badge
        self.badge_beginner.assign_badge()
        self.assertTrue(self.badge_beginner.earned)
        self.assertIsNotNone(self.badge_beginner.date_earned)
        self.assertIsInstance(self.badge_beginner.date_earned, datetime)

    def test_badge_assignment_flow(self):
        # Simule un utilisateur avec 50 XP, vérif que le badge n'est pas attribué
        user_xp = 50
        if self.badge_beginner.check_criteria(user_xp):
            self.badge_beginner.assign_badge()
        self.assertFalse(self.badge_beginner.earned)

        # Simule un utilisateur avec 150 XP, vérif que le badge est attribué
        user_xp = 150
        if self.badge_beginner.check_criteria(user_xp):
            self.badge_beginner.assign_badge()
        self.assertTrue(self.badge_beginner.earned)
        self.assertIsNotNone(self.badge_beginner.date_earned)

    def test_str_representation(self):
        # Vérif la représentation en chaîne du badge avant attribution
        self.assertEqual(
            str(self.badge_beginner),
            "Badge: Beginner, Description: Earned for reaching 100 XP, Date Earned: None"
        )

        # Attribution du badge
        self.badge_beginner.assign_badge()
        # Vérif la représentation en chaîne du badge après attribution
        self.assertIn("Date Earned: ", str(self.badge_beginner))

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)