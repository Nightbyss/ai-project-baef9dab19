## ---FILE: main.py---

```
# main.py
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot
import logging
from datetime import datetime
from random import choice
from typing import Dict, List
import json
import requests

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context):
    """Start command handler."""
    update.message.reply_text('Привет! Я бот для фитнеса и ИИ-интеграции.\n'
                              'Могу помочь составить план тренировок, подсказать упражнения '
                              'или рассказать про правильное питание.')

def help_command(update: Update, context):
    """Help command handler."""
    update.message.reply_text('Вот мои команды:\n'
                               '/start - начать работу\n'
                               '/help - показать список команд\n'
                               '/train - получить тренировочный план\n'
                               '/food - узнать про правильное питание')

def train(update: Update, context):
    """Send training plan to user."""
    response = get_training_plan()
    if response:
        update.message.reply_text(response)

def food(update: Update, context):
    """Send info about healthy eating."""
    update.message.reply_text(get_food_info())

def get_training_plan() -> str:
    """Get a training plan from API and return it as text."""
    try:
        # Call the OpenAI API for generating a fitness plan
        response = requests.post(
            url="https://api.openai.com/v1/engines/davinci/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "prompt": "Составь тренировочный план для человека среднего уровня подготовки.",
                "max_tokens": 500,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['text']
    except Exception as e:
        logger.error(f"Error getting training plan: {e}")
        return "Упс, кажется, сейчас сервис недоступен."

def get_food_info() -> str:
    """Return some information on healthy eating."""
    return "Для правильного питания важно сбалансированное меню: овощи, фрукты, белок, "
           "сложные углеводы и полезные жиры. Пейте достаточно воды!"

def handle_message(update: Update, context):
    """Handle general messages."""
    message = update.message.text.lower()
    if "привет" in message or "hello" in message:
        update.message.reply_text("Привет! Чем займёмся?")
    elif "какие упражнения" in message:
        update.message.reply_text(get_exercises())
    else:
        update.message.reply_text("Не совсем понял тебя. Могу помочь с тренировочным планом или питанием.")

def get_exercises() -> str:
    """Get exercise suggestions using OpenAI API."""
    try:
        response = requests.post(
            url="https://api.openai.com/v1/engines/davinci/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "prompt": "Предложи несколько упражнений для тренировки верхней части тела.",
                "max_tokens": 200,
                "temperature": 0.8
            }
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['text']
    except Exception as e:
        logger.error(f"Error getting exercises: {e}")
        return "Упс, кажется, сейчас сервис недоступен."

def error_handler(update: Update, context):
    """Log errors caused by updates."""
    logger.error(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("train", train))
    dispatcher.add_handler(CommandHandler("food", food))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Error handling
    dispatcher.add_error_handler(error_handler)

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
```

---END---

## ---FILE: requirements.txt---

```
python-telegram-bot==13.6
requests==2.28.1
openai==0.29.4
dotenv==1.0.0
```

---END---

## ---FILE: README.md---

```
# Telegram Fitness Bot with AI Integration

This is a simple Telegram bot designed for fitness enthusiasts. It provides basic functionalities like:

- **Training Plans**: Generates personalized workout plans based on your needs.
- **Nutrition Advice**: Provides tips on healthy eating and balanced diets.
- **Exercise Ideas**: Offers suggestions for various workouts.

### Installation

To run this bot locally, follow these steps:

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root directory and add the following variables:
   ```
   TELEGRAM_TOKEN=<your_token>
   OPENAI_API_KEY=<your_openai_api_key>
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

### Usage

Once the bot is running, you can interact with it via Telegram by sending commands such as `/start`, `/help`, `/train`, and `/food`.

---
```

---END---