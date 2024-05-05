from src.admin import crud


if __name__ == "__main__":
    chat_id = input()
    crud.add_admin(chat_id)
