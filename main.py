import json
import os
import random

from dotenv import load_dotenv
from telebot.types import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	KeyboardButton,
	ReplyKeyboardMarkup
)
import telebot


JSON_FILES_DIR = "json"
SONG_LIBRARY_PATH = f"./{JSON_FILES_DIR}/music.json"
BOT_PHRASES_PATH = f"./{JSON_FILES_DIR}/phrases.json"

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT = telebot.TeleBot(TOKEN, parse_mode="Markdown")


def get_data_from_json(filepath: str):
	with open(filepath, "r", encoding="utf-8") as file:
		data = json.load(file)
	return data


def create_reply_keyboard(buttons: list):
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	for button in buttons:
		markup.add(KeyboardButton(button))
	return markup


def create_inline_button(button_text: str, playlist_link: str):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton(button_text, playlist_link))
	return markup


def bot_send_phrase_with_keyboard(chat_id, phrase_type: str):
	phrase = phrases[phrase_type]

	reply_markup = create_reply_keyboard(phrase["buttons"])
	BOT.send_message(chat_id, phrase["text"], reply_markup=reply_markup)


def bot_send_playlist(chat_id, playlist):
	random_phrases = phrases["playlist"]
	random_phrase = random.choice(random_phrases).format(
		playlist_name=playlist["name"],
		playlist_feature=playlist["feature"]
	)

	inline_markup = create_inline_button(
		"Слушать на Я.Музыке",
		playlist["link"]
	)
	BOT.send_message(chat_id, random_phrase, reply_markup=inline_markup)


@BOT.message_handler(commands=["start"])
def bot_start(message):
	bot_send_phrase_with_keyboard(message.chat.id, "greeting")


@BOT.message_handler(content_types=["text"])
def bot_define_command(message):
	if message.text == "По жанру":
		bot_send_phrase_with_keyboard(message.chat.id, "genres")
	elif message.text == "По настроению":
		bot_send_phrase_with_keyboard(message.chat.id, "moods")
	elif message.text == "Нейромузыка":
		bot_send_playlist(message.chat.id, song_library["neuro"])

	elif message.text == "Классика":
		bot_send_playlist(message.chat.id, song_library["classic"])
	elif message.text == "Поп-музыка":
		bot_send_playlist(message.chat.id, song_library["pop"])
	elif message.text == "Фонк":
		bot_send_playlist(message.chat.id, song_library["phonk"])
	elif message.text == "Американский рок":
		bot_send_playlist(message.chat.id, song_library["american_rock"])

	elif message.text == "Энергичная":
		bot_send_playlist(message.chat.id, song_library["pop"])
	elif message.text == "Философская":
		bot_send_playlist(message.chat.id, song_library["philosophy"])
	elif message.text == "Страшная":
		bot_send_playlist(message.chat.id, song_library["scary"])


if __name__ == "__main__":
	song_library = get_data_from_json(SONG_LIBRARY_PATH)
	phrases = get_data_from_json(BOT_PHRASES_PATH)

	BOT.infinity_polling()
