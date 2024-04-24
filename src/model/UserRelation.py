from src import bot


class UserRelation:
    def __init__(self, user_id, other_user_id, relation):
        self.user_id = user_id
        self.other_user_id = other_user_id
        self.relation = relation
        self.search_dislike = "Дизлайк"
        self.search_skip = "Пропустить"
        self.search_like = "Лайк"
        self.relation_to_db_alias = {
            self.search_dislike: "BLACKLIST",
            self.search_skip: "SKIPPED",
            self.search_like: "FOLLOW",
        }

    def add_relation(self):
        cursor = bot.DBController().cursor
        cursor.execute(
            f"SELECT * FROM tele_meet_relations WHERE user_id = {self.user_id} AND other_user_id = {self.other_user_id}"
        )
        existing_relation = cursor.fetchone()
        if existing_relation:
            cursor.execute(
                f"UPDATE tele_meet_relations SET relation = '{self.relation_to_db_alias[self.relation]}' WHERE "
                f"user_id = {self.user_id} AND other_user_id = {self.other_user_id}"
            )
        else:
            cursor.execute(
                f"INSERT INTO tele_meet_relations (user_id, other_user_id, relation) VALUES ({self.user_id}, "
                f"{self.other_user_id}, '{self.relation_to_db_alias[self.relation]}')"
            )
        if self.relation == self.search_like:
            query = (
                f"SELECT * FROM tele_meet_relations WHERE user_id = {self.other_user_id} "
                f"AND other_user_id = {self.user_id} AND relation = 'FOLLOW'"
            )
            bot.DBController().cursor.execute(query)
            other_user_rows = bot.DBController().cursor.fetchall()
            if other_user_rows:
                self.add_match()
                other_user_row = other_user_rows[-1]
                other_relation = other_user_row[3]
                return other_relation == "FOLLOW"
        else:
            self.remove_match()
        return False

    def match_select_one(self):
        cursor = bot.DBController().cursor
        cursor.execute(
            f"SELECT * FROM tele_meet_match WHERE user_id = {self.user_id} AND other_user_id = {self.other_user_id}"
        )
        return cursor.fetchone()

    def add_match(self):
        existing_match = self.match_select_one()
        if not existing_match:
            cursor = bot.DBController().cursor
            cursor.execute(
                f"INSERT INTO tele_meet_match (user_id, other_user_id) VALUES ({self.user_id}, {self.other_user_id})"
            )
            cursor.execute(
                f"INSERT INTO tele_meet_match (user_id, other_user_id) VALUES ({self.other_user_id}, {self.user_id})"
            )

    def remove_match(self):
        existing_match = self.match_select_one()
        if existing_match:
            cursor = bot.DBController().cursor
            cursor.execute(
                f"DELETE FROM tele_meet_match WHERE user_id = {self.user_id} AND other_user_id = {self.other_user_id})"
            )
            cursor.execute(
                f"DELETE FROM tele_meet_match WHERE user_id = {self.other_user_id} AND other_user_id = {self.user_id})"
            )
