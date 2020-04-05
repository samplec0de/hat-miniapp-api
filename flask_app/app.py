from logging.config import dictConfig
import random

from flask_pymongo import PyMongo

from AppUser import AppUser
from flask import Flask, jsonify
from pathlib import Path
from utility import get_words

from yaml import safe_load

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
config = safe_load((Path(__file__).parent / "config.yml").read_text())
app.config["MONGO_URI"] = f"mongodb://{config['mongo']['user']}:" \
                          f"{config['mongo']['password']}@{config['mongo']['host']}:" \
                          f"{config['mongo']['port']}/{config['mongo']['authdb']}"
flask_mongo = PyMongo(app)
client = flask_mongo.cx
words = set(get_words())


@app.route('/')
def hello_world():
    return ''


@app.route('/words/<vk_user_id>', methods=['GET'])
def get_random_word(vk_user_id: str):
    if not vk_user_id.isdigit():
        return jsonify({'error': 'user id not an integer'}), 400
    user = AppUser(vk_id=int(vk_user_id), mongo=client)
    user_words = set(user.get_words())
    available_words = list(words.difference(user_words))
    if available_words:
        word = random.choice(available_words)
        user.give_word(word=word)
        return jsonify({'word': word}), 200
    else:
        return jsonify({'error': 'there are no available words for user'}), 404


if __name__ == '__main__':
    app.run()
