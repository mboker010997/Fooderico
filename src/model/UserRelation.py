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
            self.search_like: "FOLLOW"
        }

    def add_relation(self):
        bot.DBController().insertQuery("tele_meet_relations",
                                   f"{self.user_id}, {self.other_user_id}, {self.relation_to_db_alias[self.relation]}")
        query = f"SELECT * FROM tele_meet_relations WHERE user_id = {self.other_user_id} AND other_user_id = {self.user_id} AND relation = {self.relation}"
        other_user_rows = DBController().cursor.execute(query).fetchall()
        if other_user_rows:
            other_user_row = other_user_rows[-1]
            other_relation = other_user_row[2]
            return other_relation == "FOLLOW" and self.relation == "FOLLOW"
        return False
