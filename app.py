from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

app = Flask(__name__)

DATABASE = os.environ.get('DATABASE')
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL is None or DATABASE is None:
    english_bot = ChatBot("English Bot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
else:
    english_bot = ChatBot("English Bot", storage_adapter="chatterbot.storage.MongoDatabaseAdapter", database=DATABASE,
                          database_uri=DATABASE_URL)

english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get/<string:query>")
def get_raw_response(query):
    return str(english_bot.get_response(query))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
