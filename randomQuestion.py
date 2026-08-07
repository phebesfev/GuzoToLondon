from telegram.ext import ContextTypes
from telegram import Update
from constants import CATEGORIES, ROUNDS
from database import init_db,pull_all_id,select_question,pull_id_withRound
import random


con = init_db()
async def randomQuestion(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chosen_round = context.args
    
    if chosen_round:
        ids = pull_id_withRound(con,chosen_round[0])

    else:
        ids = pull_all_id(con)
    
    if ids:  
        id_number = random.choice(ids)
        question = select_question(con, id_number)
        if question:
            text, round_, category = question
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'{text}\n\nRound: {ROUNDS[round_]}\nCategory: {CATEGORIES[category]}',
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'No questions found for round "{chosen_round[0] if chosen_round else "unknown"}". Valid rounds: phone, 1, 2, 3, final',
        )
    
# the plan is 
#1.take the command handler /random, the same as before
# 2. update randonQuestion Function to accept if there are words after /random or not, by checking if the argument has something or not
# 3.if empty it will be the same as prev
# 4.if not, check the actual argument, then if for example 2, we make it both id+round if round exists




