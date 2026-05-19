# v2 
import os
import telebot
import anthropic
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

bot = telebot.TeleBot(TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

historiques = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bonjour ! Je suis ton assistant IA. Comment puis-je t'aider ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    uid = message.from_user.id
    if uid not in historiques:
        historiques[uid] = []
    historiques[uid].append({"role": "user", "content": message.text})
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=historiques[uid]
    )
    texte = response.content[0].text
    historiques[uid].append({"role": "assistant", "content": texte})
    bot.reply_to(message, texte)

bot.polling()
