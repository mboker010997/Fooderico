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
        relation_info = {
            "user_id": self.user_id,
            "other_user_id": self.other_user_id,
            "relation": self.relation_to_db_alias[self.relation],
        }
        bot.DBController().insertQuery("tele_meet_relations", relation_info)
        if self.relation == self.search_like:
            query = (f"SELECT * FROM tele_meet_relations WHERE user_id = {self.other_user_id} "
                     f"AND other_user_id = {self.user_id} AND relation = 'FOLLOW'")
            bot.DBController().cursor.execute(query)
            other_user_rows = bot.DBController().cursor.fetchall()
            if other_user_rows:
                other_user_row = other_user_rows[-1]
                other_relation = other_user_row[3]
                return other_relation == "FOLLOW"
        return False
