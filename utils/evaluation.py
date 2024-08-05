import json
import random
from database.db import SQLiteDb


class Evaluation:
    def __init__(self) -> None:
        self.categories = {"family": 5, "depression": 4}

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

    def get_recomendation(self, user_id):
        db = SQLiteDb()
        clinics_chiclayo = [
            "Centro de apoyo 1:\nhttps://maps.app.goo.gl/y6Wbutb8dEBW9MUh6",
            "Centro de apoyo 2:\nhttps://maps.app.goo.gl/tESt3dmjdtLBeRYL7",
            "Centro de apoyo 3:\nhttps://maps.app.goo.gl/2jkLQJdDMwMJEyAC8",
            "Centro de apoyo 4:\nhttps://maps.app.goo.gl/7iM4tReLop8X4feb7",
        ]

        questions = db.get_evaluations_for_user(user_id)

        family = 0
        depression = 0

        for qu in questions:
            question = self.get_question_json(qu["question_id"])
            if question["category"] == "family":
                family += qu["score"]
            elif question["category"] == "depression":
                depression += qu["score"]

        if family < 5 or depression > 0:
            random_clinic = random.choice(clinics_chiclayo)
            return f"\nAsí mismo, Te recomiendo buscar apoyo en {random_clinic}"
        else:
            return ""
