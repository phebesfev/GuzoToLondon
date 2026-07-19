from telegram.ext import ConversationHandler,CommandHandler,ContextTypes,ApplicationBuilder,MessageHandler,filters
from telegram import Update,ReplyKeyboardRemove,ReplyKeyboardMarkup
from dotenv import load_dotenv
import os
from uuid import uuid4
from embedding import toVector
from embedding import cosineSimilarity

from database import insert_question,init_db,insert_related_question,get_embedding

load_dotenv()
API_TOKEN = str(os.environ.get("API_TOKEN"))

QUESTION,ROUND,CATEGORY = range(3)


con = init_db()
async def submit(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "please enter the question description here"
    )
    return QUESTION

async def question_received(update:Update, context:ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text(
        "please enter the round of the question you entered"
    )
     context.user_data['question'] = update.message.text
     return ROUND
 
async def round_recived(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "please enter the category of the question you entered"
    )
    context.user_data['round'] = update.message.text

    return CATEGORY
 
   
async def category_recived(update:Update, context:ContextTypes.DEFAULT_TYPE):

    context.user_data['category'] = update.message.text

    question = context.user_data["question"]
    round = context.user_data["round"]
    category = context.user_data["category"]
    user = update.effective_user.id
    embedding = toVector(question)
  
    
    new_id = insert_question(con,question,round,category,embedding,user)
    vec = get_embedding(con)
    
    for i in range(len(vec)):
        if vec[i][0] == new_id:
            continue
        similarity_score = cosineSimilarity(embedding,vec[i][1])
        if similarity_score > 0.75:
            insert_related_question(con,new_id,vec[i][0],similarity_score)
   
    context.user_data.clear()
    return ConversationHandler.END
    
async def cancel(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bye hope we will talk soon lol",reply_markup = ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END
    

def main(): 
    application = ApplicationBuilder().token(API_TOKEN).build()
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
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == "__main__":
    main()