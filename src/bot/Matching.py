from src import bot
from src.model.Status import Status
import re
from src.algo.TagsExtraction import extract_tags_from_text


class MatchingClass:
    __initialized = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MatchingClass, cls).__new__(cls)
        return cls.instance

    def getTagsFromAboutText(self, id):
        user = bot.DBController().getUser(id)
        about_text = user.about
        lang_code = user.language_code
        return ",".join(extract_tags_from_text(about_text, lang_code))

    def matchOneTag(self, first_answers, second_answers):
        list_first_answers = re.split(", |,", first_answers)
        list_second_answers = re.split(", |,", second_answers)

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
        current_id = current_tags[0]
        current_about_tags = self.getTagsFromAboutText(current_id)

        list_of_tags = bot.DBController().getTags()

        available_users_for_match = self.deleteUsersRelations(
            bot.DBController().getIdByChatId(chat_id),
            [person_tags[0] for person_tags in list_of_tags],
        )

        matching_queue = []
        for person_tags in list_of_tags:
            other_id = person_tags[0]
            if other_id not in available_users_for_match:
                continue
            count_matches = 0
            for tag_position in range(1, len(person_tags)):
                count_matches += self.matchOneTag(
                    person_tags[tag_position], current_tags[tag_position]
                )

            other_about_tags = self.getTagsFromAboutText(other_id)
            count_matches += self.matchOneTag(
                current_about_tags, other_about_tags
            ) * 0.5
            matching_queue.append((count_matches, other_id))
        matching_queue.sort(reverse=True)
        return matching_queue[0][1] if matching_queue else None

    def deleteUsersRelations(self, id, list_of_users):
        list_of_relations = bot.DBController().getUserRelationsIds(id)

        list_of_relations = [
            relations_id[0] for relations_id in list_of_relations
        ]

        updated_list_of_users = []

        for user_id in list_of_users:
            if (
                (list_of_relations is None or user_id not in list_of_relations)
                and user_id != id
                and bot.DBController().getUserStatus(user_id)[0]
                == "status_enabled"
            ):
                updated_list_of_users.append(user_id)
        return updated_list_of_users
