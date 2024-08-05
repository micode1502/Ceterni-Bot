from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse

from utils.chat_gpt import CeterniChat
from utils.evaluation import Evaluation
from utils.utils import Utils

app = Flask(__name__)


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    user_number = request.values.get("From", "")
    user_name = request.values.get("ProfileName", "")

    user = {
        "name": user_name,
        "phone_number": user_number,
    }

    utils = Utils()

    user_db = utils.get_or_create_user(user)

    print(f"User: {user_db}")

    if user_db["progress"] < 10:
        question = utils.send_question(user, incoming_msg)

        if question is not None:
            msg.body(question)
        else:
            if user_db["progress"] == 9:
                eva = Evaluation()
                rec = ""
                try:
                    eva = Evaluation()
                    rec = eva.get_recomendation(user_db["id"])
                except Exception as e:
                    print(f"Error saving evaluation: {e}")
                    rec = ""

                answer = (
                    "Muchas gracias, por tus respuestas, ahora puedes decirme come te sientes de manera libre."
                    + rec
                )
                utils.db.update_user_progress(11, user_db["phone_number"])
                msg.body(answer)
    else:
        ceterni_chat = CeterniChat()
        response, gif_data = ceterni_chat.conversation(message=incoming_msg)

        if gif_data:
            try:
                msg.media("https://cataas.com/cat")
            except Exception as e:
                print(f"Error sending gif: {e}")

        msg.body(response)

    return str(resp)


@app.route("/gifs/<category>/<filename>")
def serve_image(category, filename):
    return send_from_directory("gifs/" + category, filename)


if __name__ == "__main__":
    app.run()
