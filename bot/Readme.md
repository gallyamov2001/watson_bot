## Install

Предварительно нужно скачать данные пакеты.

```bash
!pip install tensorflow 

!pip install transformers datasets 

!pip install lxml 

!pip install bs4 

!pip install torch 

!pip install requests 

!pip install telebot
```

Для запуска файла введите в консоли
```bash
!python bot.py.
```

Рабочий бот: https://t.me/watson_beta_bot

Возможные команды для бота: `/start` - перезапускает бота
                            `/link` - меняет ссылку на документацию
                            `/model` - меняет модель между базовой и дообученной.
                            
Как проходит общение с ботом:
1. Пишете `/start` либо нажимаете кнопку `/start`
2. Выбераете `/model_base` или `/model_finetuned`
3. Вводите команду `/link` для отправки ссылки на документацию
4. Задаете вопрос и получаете ответ

Также можно менять модель, ссылку в любой момент, если ввести `/model` или `/link` соотвественно.
                            
При возникновении неполадок пропишите `/start`.
