from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler, ConversationHandler,MessageHandler,filters,CallbackQueryHandler
from randomQuestion import randomQuestion
from submit import interrupt_with, restart_submit, submit,question_received,round_recived,category_recived,cancel
import httpx
from telegram.request import HTTPXRequest
from search import search
from filtering_and_buttons import backToFilter, doneFilter, show_round_options,filterMenu,show_category_options,chooseFilter,chooseRound,chooseCategory


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
        text = (
            "👋 Welcome to Professor Bot — your Bloomberg interview prep tracker!\n\n"
            "Here's what I can do:\n\n"
            "📝 /submit — Add a new interview question\n"
            "🔍 /search <keywords> — Search by keyword or meaning\n"
            "🗂 /filter — Browse questions by round or category\n"
            "🎲 /random — Get a random question  (/random <round> for a specific round)\n"
            "❌ /cancel — Cancel the current operation\n\n"
            "Type any command to get started!"
        )
    )
    
# echoing function
async def parrot(update:Update, context:ContextTypes.DEFAULT_TYPE):
    #print(id(context.bot))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = update.message.text,
    )
    
QUESTION,ROUND,CATEGORY = range(3)    
# adding error handler just as claude suggested
async def error_handler(update,context):
    logging.error('Exception while handling an update:',exc_info=context.error)
    
    if isinstance(update,Update):
        try:
            if update.callback_query:
                await update.callback_query.answer('something went wrong,please try again')
            elif update.effective_chat:
                await context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = 'sorry, something went wrong. please try again.'
                )
            
        except Exception:
            pass
        
    
fallbacks=[
    CommandHandler("cancel", cancel),
    CommandHandler("filterMenu", interrupt_with(filterMenu)),
    CommandHandler("search", interrupt_with(search)),
    CommandHandler("random", interrupt_with(randomQuestion)),
    CommandHandler("start",  interrupt_with(start)),
    CommandHandler("submit", restart_submit),
]
 
    
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
                ROUND:[CallbackQueryHandler(round_recived, pattern='^sub_round:')],
                CATEGORY:[CallbackQueryHandler(category_recived, pattern='^sub_cat:')]
                },
            fallbacks=fallbacks,
        )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT&(~filters.COMMAND),parrot))
    application.add_handler(CommandHandler('random',randomQuestion))
    application.add_handler(CommandHandler('search',search))
    application.add_handler(CommandHandler('filter',filterMenu))

    # for search
    application.add_handler(CallbackQueryHandler(chooseFilter, pattern='^(roundchoice|categorychoice)$'))
    application.add_handler(CallbackQueryHandler(chooseRound,    pattern='^round:'))
    application.add_handler(CallbackQueryHandler(chooseCategory, pattern='^cat:'))
    
    application.add_handler(CallbackQueryHandler(backToFilter, pattern='^back$'))
    application.add_handler(CallbackQueryHandler(doneFilter,pattern='^done$'))

    application.add_error_handler(error_handler)


    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
