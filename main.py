from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler, ConversationHandler,MessageHandler,filters,CallbackQueryHandler
from randomQuestion import randomQuestion
from submit import submit,question_received,round_recived,category_recived,cancel
import httpx
from telegram.request import HTTPXRequest
from search import search
from filtering_and_buttons import show_round_options,filter,show_category_options,chooseFilter,chooseRound,chooseCategory


load_dotenv()
API_TOKEN = str(os.environ.get("API_TOKEN"))

import logging
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# send hey on /start command
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    #print(id(context.bot))
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "hey I am a bot, talk to me about anything lol"
    )
    
# echoing function
async def parrot(update:Update, context:ContextTypes.DEFAULT_TYPE):
    #print(id(context.bot))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = update.message.text,
    )
    
    

QUESTION,ROUND,CATEGORY = range(3)   
    
if __name__ == "__main__":
    request = HTTPXRequest(
    httpx_kwargs={"transport": httpx.AsyncHTTPTransport(local_address="0.0.0.0")}
    )
    application  = ApplicationBuilder().token(API_TOKEN).request(request).build() 
    application.add_handler(CommandHandler('start',start))
    conv_handler = ConversationHandler(
            entry_points= [CommandHandler("submit",submit)],
            states={
                QUESTION:[MessageHandler(filters.TEXT & ~ filters.COMMAND,question_received)],
                ROUND:[MessageHandler(filters.TEXT & ~ filters.COMMAND,round_recived)],
                CATEGORY:[MessageHandler(filters.TEXT & ~ filters.COMMAND,category_recived)]
                },
            fallbacks=[CommandHandler("cancel",cancel)],
        )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT&(~filters.COMMAND),parrot))
    application.add_handler(CommandHandler('random',randomQuestion))
    application.add_handler(CommandHandler('search',search))
    application.add_handler(CommandHandler('filter',filter))
    # application.add_handler(CommandHandler('round',show_round_options))
    # application.add_handler(CommandHandler('category',show_category_options))
    
    application.add_handler(CallbackQueryHandler(chooseFilter, pattern='^(roundchoice|categorychoice)$'))
    application.add_handler(CallbackQueryHandler(chooseRound,    pattern='^round:'))
    application.add_handler(CallbackQueryHandler(chooseCategory, pattern='^cat:'))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
