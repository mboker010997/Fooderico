preferencesTags = [
    "tag_allergy_food_intolerance",
    "tag_vegetable_food",
    "tag_weight_loss",
    "tag_mass_retention",
    "tag_weight_gain",
    "tag_diabetes",
    "tag_pregnancy",
    "tag_lure",
    "tag_preparation",
]

restrictionsTags = [
    "tag_allergy_to_cows_milk_protein",
    "tag_allergy_to_wheat_and_cereals",
    "tag_egg_allergy",
    "tag_allergy_to_soy_lupine_and_legumes",
    "tag_allergy_to_fish_and_seafood",
    "tag_allergy_to_nuts_and_peanuts",
    "tag_allergy_to_celery_sesame_mustard",
    "tag_reaction_to_sulfur_oxide_monosodium_glutamate",
]

dietsTags = [
    "tag_vegetarianism",
    "tag_pescetarianism",
    "tag_veganism",
    "tag_raw_food",
    "tag_low_sugar_carb",
    "tag_high_protein",
]

interestsTags = [
    "tag_sport_fitness",
    "tag_dancing",
    "tag_reading",
    "tag_music",
    "tag_drawing",
    "tag_creation",
    "tag_computer_games",
    "tag_cooking",
    "tag_films_series",
]

nothing_tag = "tag_nothing_of_this"


def getReadableTagsDescription(tags, config):
    if tags is None or len(tags) == 0:
        return config.get_message("no_tags")
    func_tag_to_str = lambda x: config.get_message(str(x))
    return ", ".join(map(func_tag_to_str, tags))
