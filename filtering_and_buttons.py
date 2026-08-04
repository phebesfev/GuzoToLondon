from telegram.ext import ContextTypes
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from database import init_db,pull_id_withRound,select_question,pull_id_withCategory
import random


con = init_db()



 
async def filter(update:Update,context:ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton('by round',callback_data='roundchoice'),
            InlineKeyboardButton('by category',callback_data='categorychoice')

        ]
    ]
    
    markup=InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('please choose filter',reply_markup=markup)



async def show_round_options(update:Update,context:ContextTypes.DEFAULT_TYPE):
    # callback_data is a one that will be sent, and the invisble part of that will be sent 
    keyboard = [
        [
            InlineKeyboardButton('round 1',       callback_data='round:1'),
        InlineKeyboardButton('round 2',       callback_data='round:2'),
        ],
        
        [InlineKeyboardButton('system design', callback_data='round:system design'),
        InlineKeyboardButton('behavioral',    callback_data='round:behavioral'),
        ],
        [InlineKeyboardButton('final round',   callback_data='round:final'),]

    ]
    # changing to a format telegram understands
    markup =InlineKeyboardMarkup(keyboard)
   
    await update.callback_query.edit_message_text('please choose one round', reply_markup=markup) 
    
async def show_category_options(update:Update,context:ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton('technical',  callback_data='cat:technical'),
            InlineKeyboardButton('behavioral', callback_data='cat:behavioral'),
        ]
    ]
    
    markup=InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text('please choose category', reply_markup=markup)

    
    

# call back query handlers
async def chooseFilter(update:Update,context:ContextTypes.DEFAULT_TYPE) :
    query = update.callback_query
    await query.answer() 
    
    
    if query.data == 'roundchoice':
        await show_round_options(update,context)
        
    elif query.data =='categorychoice':
        await show_category_options(update,context)
        
async def chooseRound(update:Update,context:ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()
    
    question_text = getQuestionRound(query.data.split(':', 1)[1])       # chooseRound
    if question_text:
        await query.edit_message_text(text=question_text)
    else:
        await query.edit_message_text(text=f'question with this round doesn\'t exist please choose another round') 
    
    
async def chooseCategory(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
     
    question_text = getQuestionCategory(query.data.split(':', 1)[1])    # chooseCategory
    if question_text:
        await query.edit_message_text(text=question_text)
    else:
        await query.edit_message_text(text=f'question with this category doesn\'t exist please choose another category') 
        
        

        

# helper functions
def getQuestionRound(round):
    chosen_round = round
    question = None
    if chosen_round:
        ids = pull_id_withRound(con,chosen_round)
        
        if ids:  
            id_number = random.choice(ids)
            question = select_question(con,id_number)
            
    return question


def getQuestionCategory(category):
    chosen_category  = category
    question = None
    
    if chosen_category:
        ids = pull_id_withCategory(con,chosen_category)
    
        if ids:  
            id_number = random.choice(ids)
            question = select_question(con,id_number)
                
        
    
    return question


                    
        
