from src.statemachine import State
from src.statemachine.state import profile
from src.model.Update import Update
from aiogram import types
from src.resources import products
from src import bot
import re
from fuzzywuzzy import fuzz
import textdistance


class ProductState(State):
    def __init__(self, context):
        super().__init__(context)
        self.type = "Like"
        self.is_question = True
        self.skip = False
        self.variants = []
        self.current_poll = 0
        self.count_polls = 0

    @staticmethod
    def tokenize(text):
        return re.findall(r'[^\w\s]+|\w+', text)

    @staticmethod
    def find_closest_words_fuzzy(input_words, word_list, threshold=75, n=10):
        closest_words = []
        for input_word in input_words:
            # Fuzzy matching
            fuzzy_matches = [word for word in word_list if fuzz.ratio(input_word, word) > threshold]
            # If no fuzzy matches, use Levenshtein distance
            if not fuzzy_matches:
                closest_words_input_word = sorted(word_list,
                                                  key=lambda x: textdistance.levenshtein.normalized_distance(input_word,
                                                                                                             x))[:n]
            else:
                closest_words_input_word = sorted(fuzzy_matches,
                                                  key=lambda x: textdistance.levenshtein.normalized_distance(input_word,
                                                                                                             x))[:n]
            closest_words.extend(closest_words_input_word)
        return closest_words

    async def process_update(self, update: Update):
        self.skip = False
        message = update.get_message()

        if self.is_question:
            if not message:
                self.skip = True
                return
            variants = []
            array = self.tokenize(message.text)
            array = [word for word in array if word != ","]
            for food in array:
                variants.extend(self.find_closest_words_fuzzy([food], products, n=3))
            self.variants = list(set(variants))
            self.is_question = False
            self.current_poll = 0
            self.count_polls = (len(self.variants) - 1) // 9 + 1
            return
        else:
            poll_answer = update.get_poll_answer()
            if poll_answer and int(poll_answer.poll_id) == int(self.context.user.active_poll_id):
                for option_id in poll_answer.option_ids:
                    if option_id == 9 or self.current_poll * 9 + option_id >= len(self.variants):
                        continue
                    query = "INSERT INTO tele_meet_products (user_id, product, type) VALUES ({}, \'{}\', {})".format(
                        self.context.user.id, self.variants[self.current_poll * 9 + option_id],
                        1 if self.type == 'Like' else -1
                    )
                    print("INSERT in products:", query)
                    bot.DBController().cursor.execute(query)
                self.current_poll += 1
                if self.current_poll == self.count_polls:
                    self.is_question = True
                    if self.type == 'Like':
                        self.type = 'Dislike'
                    else:
                        self.context.set_state(profile.FoodPreferencesTagState(self.context))
                self.context.save_to_db()
            else:
                self.skip = True

    async def send_message(self, update: Update):
        if self.skip:
            return

        if self.type == 'Like':
            if self.is_question:
                if not update.get_message():
                    return
                message = update.get_message()
                text = self.context.get_message("favourite_products")
                await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
            else:
                if (self.current_poll + 1) * 9 <= len(self.variants):
                    options = self.variants[self.current_poll * 9:(self.current_poll + 1)*9]
                else:
                    options = self.variants[self.current_poll * 9:]
                options.append(self.context.get_message("tag_nothing_of_this"))

                poll_info = await update.bot.send_poll(
                    chat_id=update.get_chat_id(),
                    question="{} / {}".format(self.current_poll + 1, (len(self.variants) - 1) // 9 + 1),
                    options=options,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                )
                self.context.user.active_poll_id = poll_info.poll.id
                self.context.save_to_db()
        elif self.type == 'Dislike':
            if self.is_question:
                text = self.context.get_message("unfavourite_products")
                await update.bot.send_message(chat_id=update.get_chat_id(), text=text)
            else:
                if (self.current_poll + 1) * 9 <= len(self.variants):
                    options = self.variants[self.current_poll * 9:(self.current_poll + 1)*9]
                else:
                    options = self.variants[self.current_poll * 9:]
                options.append(self.context.get_message("tag_nothing_of_this"))

                poll_info = await update.bot.send_poll(
                    chat_id=update.get_chat_id(),
                    question="{} / {}".format(self.current_poll + 1, (len(self.variants) - 1) // 9 + 1),
                    options=options,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                )
                self.context.user.active_poll_id = poll_info.poll.id
                self.context.save_to_db()
