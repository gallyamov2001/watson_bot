import time
import logging
import telebot
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag

blocks = ["p", "h1", "h2", "h3", "h4", "h5", "blockquote"]
from transformers import pipeline

def _extract_blocks(parent_tag) -> list:
    extracted_blocks = []
    for tag in parent_tag:
        if tag.name in blocks:
            extracted_blocks.append(tag)
            continue
        if isinstance(tag, Tag):
            if len(tag.contents) > 0:
                inner_blocks = _extract_blocks(tag)
                if len(inner_blocks) > 0:
                    extracted_blocks.extend(inner_blocks)
    return extracted_blocks

def to_plaintext(html_text: str) -> str:
    soup = BeautifulSoup(html_text, features="lxml")
    extracted_blocks = _extract_blocks(soup.body)
    extracted_blocks_texts = [block.get_text().strip() for block in extracted_blocks]
    return "\n".join(extracted_blocks_texts)

def get_text(url):
    page = requests.get(url)
    text = to_plaintext(page.text)
    return text

TOKEN = "5763564557:AAH0T-sppqIrHu2QQ0vbTZ5AzeiUFDwLcDk"
MSG = "watson dead"

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(TOKEN)
link = ""
text = ""

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        user_id = message.from_user.id
        user_name = message.from_user.first_name        
        bot.send_message(message.from_user.id, "Привет," + user_name + "! Напиши /link");
        bot.register_next_step_handler(message, get_link); #следующий шаг – функция get_link
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')
def get_link(message):
    if message.text == '/link':
        bot.send_message(message.from_user.id, "Отправь ссылку на документацию.");
        bot.register_next_step_handler(message, mainfunc); #следующий шаг – main_func
    else:
        bot.send_message(message.from_user.id, 'Напиши /link')

def mainfunc(message):
    global link
    global text
    link = message.text
    if len(link) > 0:
        text = get_text(link)
        bot.send_message(message.from_user.id, "Отлично, теперь задай вопрос")
        bot.register_next_step_handler(message, func_ans); #следующий шаг – func_ans
    else:
        bot.send_message(message.from_user.id, 'Я не вижу ссылку...')
        

def func_ans(message):
    model = pipeline(model='AndrewChar/model-QA-5-epoch-RU')
    question = message.text
    answer = model(context=text, question=question)
    #answer = "ссылка: " + link + " вопрос: " + question + text[:100]
    #answer = text[100:300]
    answer = answer['answer']
    bot.send_message(message.from_user.id, question)    
    bot.send_message(message.from_user.id, answer)
    bot.send_message(message.from_user.id, "Какое еще вопрос?")
    bot.register_next_step_handler(message, func_ans)

bot.infinity_polling()
