#это самая первая версия бота, которая была

import requests
from bs4 import BeautifulSoup
from transformers import pipeline


def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    article = root.select_one('article')

    return article.text




print("Введите ссылку на документацию в html формате:")
url = input()
text = get_text(url)

try:
    while True:
        model = pipeline(model='AndrewChar/model-QA-5-epoch-RU')
        print("Введите вопрос...")
        question = input()
        answer = model(context=text, question=question)
        print(answer['answer'])

except KeyboardInterrupt:
    print('Finished!\n')

