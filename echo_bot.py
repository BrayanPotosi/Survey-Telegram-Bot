from flask import Flask
import telebot
import json


bot = telebot.TeleBot(
    "Telegram_key", parse_mode=None)

app = Flask(__name__)


"""Open the questions file"""
with open('questions.json', 'r') as question_file:
    data = question_file.read()

"""Decoding Json"""
questions_file = json.loads(data)

"""/start initial welcome message """
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Bienvenido a esta encuesta \n {questions_file['welcome_message']}")

"""send and get user data"""
@bot.message_handler(func=lambda m: True)
def echo_all(message):

    """responding to the user"""
    bot.reply_to(message, message.text)

    """getting a str id from the user data"""
    id_user = str(message.from_user.id)

    last_answer = get_last_question_from_user(id_user)
    last_question_id = last_answer["id_question"]

    if last_question_id == "":

        """if dont exist an answer for that user then """
        save_response(id_user, 0 , message.text)
        send_next_question(-1, message)

    else: 
        save_response(id_user, last_answer["id_question"] + 1 , message.text)
        send_next_question(last_question_id, message)


"""reading the last questionn of an user"""
def get_last_question_from_user(id):

    with open('answers.json', 'r') as answers_file:
        data = answers_file.read()

    answers_file = json.loads(data)

    if id in answers_file:
        last_answer = answers_file[id][-1]
    else:
        return {
                "id_question": "",
                "answer_content": ""
            }

    return last_answer


"""processing the response on answers.json file"""
def save_response(id_user, id_question, message_content):

    with open('answers.json', 'r') as answers_file:
        data = answers_file.read()

    answers_json = json.loads(data)

    """if the user dont exist in the file then the user is created"""
    if id_user not in answers_json:
        answers_json[id_user] = []
    answers_json[id_user].append({"id_question": id_question, "message_content": message_content})

    json_datax = json.dumps(answers_json, indent=4)

    """writing the response on the json file"""
    with open('answers.json', 'w') as answers_file:
        answers_file.write(json_datax)

    """sending a new question to the user"""
def send_next_question(id_question, message):

    current_question = questions_file["questions"][id_question + 1]
    bot.reply_to(message, current_question)


bot.polling()

