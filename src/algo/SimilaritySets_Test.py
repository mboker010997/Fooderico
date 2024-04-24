from src.algo.SimilaritySets import similarity
from src.model import User
from src.statemachine import Context
import unittest
from src.model import Localization


class TestSimilarity(unittest.TestCase):
    def test_similarity_simple(self):
        user = User()
        other_user = User()
        user.preferences_tags = [
            'tag_vegetable_food',
            'tag_diabetes',
            'tag_lure',
        ]
        user.restrictions_tags = [
            'tag_egg_allergy',
            'tag_allergy_to_nuts_and_peanuts',
            'tag_allergy_to_fish_and_seafood',
        ]
        user.dietary = ['tag_raw_food', 'tag_vegetarianism']
        user.interests_tags = ['tag_music']

        other_user.preferences_tags = [
            'tag_allergy_food_intolerance',
            'tag_diabetes',
            'tag_pregnancy',
        ]
        other_user.restrictions_tags = [
            'tag_allergy_to_fish_and_seafood',
        ]
        other_user.dietary = ['tag_low_sugar_carb', 'tag_high_protein']
        other_user.interests_tags = ['tag_dancing', 'tag_music']

        Localization.load_info()
        context = Context('ru')
        similar_tags_str = similarity(user, other_user, context)
        similar_set = set(similar_tags_str.split(', '))
        expected_list = [
            context.get_message('tag_diabetes'),
            context.get_message('tag_allergy_to_fish_and_seafood'),
            context.get_message('tag_music'),
        ]
        expected_set = set(expected_list)
        self.assertEqual(expected_set, similar_set,
                         "Similarity function returns wrong answer")


if __name__ == "__main__":
    unittest.main()
