from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler,MessageHandler,filters

load_dotenv()
API_TOKEN = str(os.environ.get("API_TOKEN"))

import logging
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# send hey on /start command
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(id(context.bot))
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "hey I am a bot, talk to me about anything lol"
    )
    
# echoing function
async def parrot(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(id(context.bot))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = update.message.text,
    )
    
    
if __name__ == "__main__":
    application  = ApplicationBuilder().token(API_TOKEN).build() 
    application.add_handler(CommandHandler('start',start))
    application.add_handler(MessageHandler(filters.TEXT&(~filters.COMMAND),parrot))
    
    application.run_polling()
    
