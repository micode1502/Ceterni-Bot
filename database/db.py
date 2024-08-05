import sqlite3


class SQLiteDb:
    def __init__(self):
        self.connection = sqlite3.connect("certeni.db")
        self.create_tables()

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            # Define SQL statements to create tables if they don't exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone_number TEXT UNIQUE NOT NULL,
                    alias TEXT,
                    progress INTEGER DEFAULT 0
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT,
                    answer TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    question_id INTEGER,
                    state INTEGER DEFAULT 0,
                    score INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """
            )
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def save_user(self, user):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL INSERT statement
            cursor.execute(
                "INSERT INTO users (name, phone_number) VALUES (?, ?)",
                (user.get("name"), user.get("phone_number")),
            )
            self.connection.commit()
            cursor.close()

            return self.get_user(user.get("phone_number"))
        except sqlite3.Error as e:
            print(f"Error saving user: {e}")
            return None

    def get_user(self, phone_number):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE phone_number=?", (phone_number,))
            user = cursor.fetchone()
            cursor.close()

            if user is None:
                return None

            user = {
                "id": user[0],
                "name": user[1],
                "phone_number": user[2],
                "alias": user[3],
                "progress": user[4],
            }
            return user
        except sqlite3.Error as e:
            print(f"Error retrieving user: {e}")
            return None

    def save_message(self, message):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL INSERT statement
            cursor.execute(
                "INSERT INTO messages (user_id, content, answer) VALUES (?, ?, ?)",
                (message.get("user_id"), message.get("content"), message.get("answer")),
            )
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error saving message: {e}")

    def get_messages_for_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL SELECT statement
            cursor.execute("SELECT * FROM messages WHERE user_id=?", (user_id,))
            messages = cursor.fetchall()
            cursor.close()

            rows = []
            for message in messages:
                message = {
                    "id": message[0],
                    "user_id": message[1],
                    "content": message[2],
                    "answer": message[3],
                }

                rows.append(message)

            return rows
        except sqlite3.Error as e:
            print(f"Error retrieving messages: {e}")
            return []

    def update_user_alias(self, alias, phone_number):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL SELECT statement
            cursor.execute(
                "UPDATE users SET alias=? WHERE phone_number=?",
                (
                    alias,
                    phone_number,
                ),
            )
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error updating user's alias: {e}")

    def update_user_progress(self, progress, phone_number):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL SELECT statement
            cursor.execute(
                "UPDATE users SET progress=? WHERE phone_number=?",
                (
                    progress,
                    phone_number,
                ),
            )
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error updating user's progress: {e}")

    def save_evaluation(self, evaluation):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL INSERT statement
            cursor.execute(
                "INSERT INTO evaluations (user_id, question_id, state) VALUES (?, ?, ?)",
                (evaluation.get("user_id"), evaluation.get("question_id"), evaluation.get("state")),
            )
            self.connection.commit()
            cursor.close()
            evaluation = self.get_evaluation(
                evaluation.get("user_id"), evaluation.get("question_id")
            )
            return evaluation
        except sqlite3.Error as e:
            print(f"Error saving evaluation: {e}")
            return None

    def get_evaluations_for_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL SELECT statement
            cursor.execute("SELECT * FROM evaluations WHERE user_id=?", (user_id,))
            evaluation = cursor.fetchall()
            cursor.close()

            rows = []
            for evaluation in evaluation:
                evaluation = {
                    "id": evaluation[0],
                    "user_id": evaluation[1],
                    "question_id": evaluation[2],
                    "state": evaluation[3],
                    "score": evaluation[4],
                }

                rows.append(evaluation)

            return rows
        except sqlite3.Error as e:
            print(f"Error retrieving evaluation: {e}")
            return []

    def update_evaluation(self, evaluation):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL SELECT statement
            cursor.execute(
                "UPDATE evaluations SET state=?, score=? WHERE user_id=? AND question_id=?",
                (
                    evaluation.get("state"),
                    evaluation.get("score"),
                    evaluation.get("user_id"),
                    evaluation.get("question_id"),
                ),
            )
            print(evaluation)
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Error updating evaluation: {e}")

    def get_evaluation(self, user_id, question_id):
        try:
            cursor = self.connection.cursor()
            # Replace the placeholders with actual SQL SELECT statement
            cursor.execute(
                "SELECT * FROM evaluations WHERE user_id=? AND question_id=?",
                (user_id, question_id),
            )
            evaluation = cursor.fetchone()

            if evaluation is None:
                return None

            evaluation = {
                "id": evaluation[0],
                "user_id": evaluation[1],
                "question_id": evaluation[2],
                "state": evaluation[3],
                "score": evaluation[4],
            }
            cursor.close()
            return evaluation
        except sqlite3.Error as e:
            print(f"Error retrieving evaluation: {e}")
            return None
