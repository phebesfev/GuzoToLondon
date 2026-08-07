from telegram.ext import ConversationHandler,CommandHandler,ContextTypes,ApplicationBuilder,MessageHandler,filters
from telegram import Update,ReplyKeyboardRemove,ReplyKeyboardMarkup
from dotenv import load_dotenv
import os
from uuid import uuid4
from embedding import toVector
from embedding import cosineSimilarity

from database import insert_question,init_db,insert_related_question,get_embedding
from constants import buildInlineKeyboard,ROUNDS,CATEGORIES
import sqlite3



QUESTION,ROUND,CATEGORY = range(3)


con = init_db()
async def submit(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Let's log a Bloomberg interview question!\n\n"
        "Type the question exactly as it was asked — be as specific as possible, "
        "it helps others find it later.\n\n"
        "Send /cancel at any time to stop."
    )
    return QUESTION

async def question_received(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data['question'] = update.message.text

    await update.message.reply_text(
        'which round was this question asked in?',
        reply_markup=buildInlineKeyboard(ROUNDS,'sub_round')
    )
    return ROUND
 
async def round_recived(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['round'] = query.data.split(':',1)[1]

    
    await query.edit_message_text(
        f'Round: {ROUNDS[context.user_data['round']]}\n\nWhich category?',
        reply_markup=buildInlineKeyboard(CATEGORIES,'sub_cat')
    )

    return CATEGORY
 
   
async def category_recived(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['category'] = query.data.split(':',1)[1]

    question = context.user_data["question"]
    round = context.user_data["round"]
    category = context.user_data["category"]
    user = update.effective_user.id
    embedding = toVector(question)
  
    try:
        new_id = insert_question(con,question,round,category,embedding,user)
        
    except sqlite3.IntegrityError:
        await query.edit_message_text('sorry, could not save that. please try /submit again')
        context.user_data.clear()
        return ConversationHandler.END
    
    
    vec = get_embedding(con)
    
    for i in range(len(vec)):
        if vec[i][0] == new_id:
            continue
        similarity_score = cosineSimilarity(embedding,vec[i][1])
        if similarity_score > 0.75:
            insert_related_question(con,new_id,vec[i][0],similarity_score)
   
    await query.edit_message_text(
        f'saved!\n\n{question}\n\n'
        f'Round: {ROUNDS[round]}\nCategory: {CATEGORIES[category]}'
    )
    
    context.user_data.clear()
    return ConversationHandler.END
    
async def cancel(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bye hope we will talk soon lol",reply_markup = None
    )
    context.user_data.clear()
    return ConversationHandler.END
    



# for fall back in commands
def interrupt_with(func):
    async def wrapper(update, context):
        context.user_data.clear()
        await func(update, context)
        return ConversationHandler.END
    return wrapper


async def restart_submit(update, context):
    context.user_data.clear()
    return await submit(update, context)      # returns QUESTION — restarts cleanly
