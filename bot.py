import os
import time
import random

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup

from config import token
from templates import *
from keyboards import make_roll_attributes

bot = telebot.TeleBot(token=token)

user_state = {}

@bot.message_handler(commands=["start"])
def start_cmd(message):
	chat_id = message.chat.id

	gif_path = os.path.join("static", "gif", "start.gif")
	if os.path.exists(gif_path):
		with open(gif_path, "rb") as gif_file:
			bot.send_animation(
		  	chat_id=chat_id,
		  	animation=gif_file,
		  	caption="Утро. Ты открываешь глаза и не понимаешь где ты. Как тебя зовут?"
			)
	else:
		bot.send_message(
		chat_id=chat_id,
		text="Утро. Ты открываешь глаза и не понимаешь где ты. Как тебя зовут?"
	  	)

	user_state[chat_id] = {
	  "step": "awaiting_name",
	  "player": player.copy()
	}

@bot.callback_query_handler(func=lambda call: call.data.startswith("roll_"))
def handle_roll_buttons(call):
	chat_id = call.message.chat.id

	attributes = call.data.split("_")[-1]

	dice_message = bot.send_dice(
	chat_id=chat_id,
	emoji="🎲"
  	)

	time.sleep(5)

	dice_message = dice_message.dice.value

	if attributes == "strenght":
		user_state[chat_id]["player"]["strenght"] = dice_message
		text = f"Твоя сила растёт! Теперь твоя сила: {dice_message}"
	elif attributes == "agility":
		user_state[chat_id]["player"]["agility"] = dice_message
		text = f"Твоя ловкость растёт! Теперь твоя ловкость: {dice_message}"
	elif attributes == "charisma":
		user_state[chat_id]["player"]["charisma"] = dice_message
		text = f"Твоя харизма растёт! Теперь твоя харизма: {dice_message}"
	elif attributes == "intellect":
		user_state[chat_id]["player"]["intellect"] = dice_message
		text = f"Твой интеллект растёт! Теперь твой интеллект: {dice_message}"

	bot.send_message(
	chat_id=chat_id,
	text=text
  	)

# Функция для расчета урона
def calculate_damage(attacker_strength, defender_armor):
	damage = attacker_strength - defender_armor
	return damage if damage > 0 else 0


# Инициализация боя
def init_battle(hero, enemy, chat_id):
	markup = quick_markup({'💥Удар💥': {'callback_data': 'attack'}}, row_width=1)

	stats_message = bot.send_message(chat_id=chat_id,
									 text=f"🥷🏼 {hero['name']} (HP: {hero['hp']}) vs 👹 {enemy['name']} (HP: {enemy['hp']})",
									 reply_markup=markup)

	user_state[chat_id]['stats_message'] = stats_message


# Обработка нажатия кнопки "Удар"
@bot.callback_query_handler(func=lambda call: call.data == 'attack')
def attack(call):
	chat_id = call.message.chat.id
	user_id = chat_id

	markup = quick_markup({'💥Удар💥': {'callback_data': 'attack'}}, row_width=1)

	stats_message = user_state[chat_id]['stats_message']

	# Определяем героя
	hero = user_state[user_id]['player']

	enemy = user_state[user_id]['enemy']

	# Моделируем бросок кубика для атаки
	dice_message = bot.send_dice(chat_id)

	# После анимации кубика нужно вычислить урон
	damage_to_enemy = calculate_damage(dice_message.dice.value + hero['strenght'], enemy['armor'])
	enemy["hp"] -= damage_to_enemy

	time.sleep(5)

	bot.send_message(chat_id=user_id,
					 text=f"{hero['name']} наносит {damage_to_enemy} урона {enemy['name']}.")

	if enemy["hp"] <= 0:
		enemy["hp"] = 0
		bot.send_message(chat_id, f"{hero['name']} победил {enemy['name']}!")

		# Удаляем информацию о противнике
		del user_state[user_id]['enemy']

		# Удаляем сообщение о статистике
		del user_state[chat_id]['stats_message']

	if hero['hp'] <= 0:
		hero['hp'] = 0
		bot.send_message(chat_id, f"{enemy['name']} победил {hero['name']}!")

	else:
		damage_to_hero = calculate_damage(enemy["strenght"], hero['armor'])
		hero['hp'] -= damage_to_hero
		bot.send_message(chat_id, f"{enemy['name']} наносит {damage_to_hero} урона {hero['name']}.")

	# Удаляем информацию о противнике
	del user_state[user_id]['enemy']

	# Удаляем сообщение о статистике
	del user_state[chat_id]['stats_message']

	# Обновляем текст сообщения с учетом урона
	bot.edit_message_text(chat_id=chat_id,
						  message_id=stats_message.message_id,
						  text=f"{hero['name']} (HP: {hero['hp']}) vs {enemy['name']} (HP: {enemy['hp']})",
						  reply_markup=markup)

	@bot.message_handler(commands=['fight'])
	def start_battle(message):
		user_id = message.chat.id
		hero = user_state[user_id]['player']
		enemy = random.choice(enemies)
		user_state[user_id]['enemy'] = enemy
		init_battle(hero, enemy, message.chat.id)

	@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id]["step"] == "awaiting_name")
	def set_character_name(message):
		print("set_character_name")
		chat_id = message.chat.id
		name = message.text

		user_state[chat_id]["player"]["name"] = name
		user_state[chat_id]["step"] = "awaiting_attributes"

		bot.send_message(
			chat_id=chat_id,
			text="Великий бог рандома дал вам выбор. Вы можете повлияеть на свои характеристики. Выберите испытание:",
			reply_markup=make_roll_attributes()
		)

bot.infinity_polling()
