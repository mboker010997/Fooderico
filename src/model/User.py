class User:
    def __init__(self):
        self.id = None  # int
        self.age = None  # int
        self.create_date = None  # ???
        self.update_date = None  # ???
        self.city = None  # string
        self.first_name = None  # string
        self.gender = None  # enum Gender
        self.geolocation = None  # class geolocation (todo: FOOD-43)
        self.language_code = None  # string
        self.last_name = None  # string
        self.phone_number = None  # string
        self.photo_file_ids = None  # list of strings
        self.profile_name = None  # string
        self.restrictions_tags = None
        self.interests_tags = None  # string set ???
        self.state_class = None  # state class (exactly class, not instance)
        self.status = None  # enum Status
        self.username = None  # string
        self.about = None  # string
        self.active_poll_id = None  # string
        self.chat_id = None  # string
        self.food_preferance_and_goals = None # string
        self.food_allergens = None # string
        self.dietary = None # string
        self.main_interests = None # string
        self.others_interests = None # string
        self.preferences_tags = None # string