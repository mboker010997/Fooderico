from src import bot
import re

class MatchingClass:
    __initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MatchingClass, cls).__new__(cls)
        return cls.instance

    def getOtherTags(self, text):
        # TODO need algorithm to get tags from text (smth like dataset)
        return ""

    def matchOneTag(self, first_answers, second_answers):
        list_first_answers = re.split(', |,', first_answers)
        list_second_answers = re.split(', |,', second_answers)

        list_first_answers.sort()
        list_second_answers.sort()

        count_matches = 0
        for answer_first in list_first_answers:
            for answer_second in list_second_answers:
                if answer_first == answer_second:
                    count_matches += 1
        return count_matches


    def tagsMatchingQueue(self, chat_id):
        current_tags = bot.DBController().getUserTags(chat_id)

        list_of_tags = bot.DBController().getTags()

        matching_queue = []
        for person_tags in list_of_tags:
            count_matches = 0
            for tag_position in range(1, len(person_tags)):
                count_matches += self.matchOneTag(person_tags[tag_position], current_tags[tag_position])
            matching_queue.append((count_matches, person_tags[0]))
        matching_queue.sort(reverse=True)
        return self.deleteUsersRelations(bot.DBController().getIdByChatId(chat_id), [id for count_matches, id in matching_queue])

    def deleteUsersRelations(self, id, list_of_users):
        list_of_relations = bot.DBController().getUserRelationsIds(id)

        list_of_relations = [relations_id[0] for relations_id in list_of_relations]

        for user_id in list_of_users:
            if (list_of_relations is None or user_id not in list_of_relations) and user_id != id:
                return user_id
        return None