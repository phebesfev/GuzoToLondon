from telegram.ext import ContextTypes
from telegram import Update
from database import init_db,pull_all_id
import random


con = init_db()
async def randomQuestion(update:Update,context:ContextTypes.DEFAULT_TYPE):
    ids = pull_all_id(con)
    question = random.choice(ids)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=question,
    )
    
    return None