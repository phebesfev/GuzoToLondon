import asyncio
import telegram
from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler

load_dotenv()
API_TOKEN = str(os.environ.get("API_TOKEN"))

import logging
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "hey I am a bot, talk to me about anything lol"
    )
            
if __name__ == "__main__":
    application  = ApplicationBuilder().token(API_TOKEN).build()
    application.add_handler(CommandHandler('start',start))
    application.run_polling()
    

# print(main())