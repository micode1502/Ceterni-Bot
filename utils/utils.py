import json
from database.db import SQLiteDb
from utils.chat_gpt import get_question_score


class Utils:
    def __init__(self):
        self.db = SQLiteDb()

    def get_or_create_user(self, user):
        user_db = self.db.get_user(user["phone_number"])
        if user_db is None:
            user_db = self.db.save_user(user)
        return user_db

    def get_question_json(self, question_id):
        """Get questions from json file."""
        with open("database/questions.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        question = next(
            (
                question
                for question in data["questions"]
                if question["id"] == question_id
            ),
            None,
        )

        return question

    def send_question(self, user, answer=None):
        user_db = self.get_or_create_user(user)

        progress = user_db["progress"]

        if progress > 9:
            return None

        current_question = self.db.get_evaluation(user_db["id"], progress)

        if progress == 0:
            evaluation = {
                "user_id": user_db["id"],
                "question_id": 1,
                "state": 0,
            }
            current_question = self.db.save_evaluation(evaluation)
            self.db.update_user_progress(1, user_db["phone_number"])
            progress = 1

        state = current_question["state"]

        if state == 0:
            question = self.get_question_json(progress)
            evaluation = {
                "score": 0,
                "user_id": user_db["id"],
                "question_id": progress,
                "state": 1,
            }
            self.db.update_evaluation(evaluation)

            return question["question"]

        elif state == 1:
            question = self.get_question_json(progress)

            evaluation = {
                "score": self.get_score(question["id"], answer),
                "user_id": user_db["id"],
                "question_id": progress,
                "state": 2,
            }
            self.db.update_evaluation(evaluation)

            evaluation = {
                "user_id": user_db["id"],
                "question_id": progress + 1,
                "state": 1,
            }
            current_question = self.db.save_evaluation(evaluation)
            self.db.update_user_progress(progress + 1, user_db["phone_number"])
            if progress < 9:
                question = self.get_question_json(progress + 1)
                return question["question"]

            return None

    def get_score(self, question_id, answer):
        if question_id < 4:
            return 0

        question = self.get_question_json(question_id)
        options = question["options"]

        formatted_options = ", ".join(
            [f"{key}: {value}" for key, value in options.items()]
        )

        gtp_score = get_question_score(question["question"], answer, formatted_options)

        return gtp_score
