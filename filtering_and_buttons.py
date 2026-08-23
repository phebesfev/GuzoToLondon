from telegram.ext import ContextTypes
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from database import init_db,pull_id_withRound,select_question,pull_id_withCategory
import random
from constants import buildInlineKeyboard,ROUNDS,CATEGORIES,buildResultKeyboard


con = init_db()

# helper function
def filterKeyboard():
    keyboard = [[
        InlineKeyboardButton('🎯 By Round',callback_data='roundchoice'),
        InlineKeyboardButton('📂 By Category', callback_data='categorychoice'),
    ]]
    markup=InlineKeyboardMarkup(keyboard)
    return markup

async def filterMenu(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('please choose filter',reply_markup=filterKeyboard())

# for the loop
async def backToFilter(update,context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text('please choose a filter',reply_markup=filterKeyboard())
    
async def doneFilter(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(query.message.text if query.message else '✅')
    
async def show_round_options(update:Update,context:ContextTypes.DEFAULT_TYPE):
    
    markup =buildInlineKeyboard(ROUNDS,'round')
   
    await update.callback_query.edit_message_text('please choose one round', reply_markup=markup) 
    
async def show_category_options(update:Update,context:ContextTypes.DEFAULT_TYPE):
  
    
    markup=buildInlineKeyboard(CATEGORIES,'cat')

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
    chose_round = query.data.split(':', 1)[1]
    context.user_data['choice'] = chose_round
    
    question_text = getQuestionRound(chose_round)       # chooseRound
    if question_text:
        await query.edit_message_text(text=f'Round: {ROUNDS[chose_round]}\n\n{question_text}',reply_markup=buildResultKeyboard())
    else:
        await query.edit_message_text(text=f'question with this round doesn\'t exist please choose another round',reply_markup=buildInlineKeyboard(ROUNDS,'round')) 
    
    
async def chooseCategory(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chosen_category = query.data.split(':', 1)[1]
    # persisting the user data until the converstaion end
    context.user_data['choice'] = chosen_category
     
    question_text = getQuestionCategory(chosen_category)    # chooseCategory
    if question_text:
        await query.edit_message_text(f'Category: {CATEGORIES[chosen_category]}\n\n{question_text}',reply_markup=buildResultKeyboard())
    else:
        await query.edit_message_text(text=f'question with this category doesn\'t exist please choose another category',reply_markup=buildInlineKeyboard(CATEGORIES,'cat')) 
        
   
async def anotherQuestion(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = context.user_data.get('choice')
    

    if choice in ROUNDS:
        question_text = getQuestionRound(choice)
        await query.edit_message_text(text=f'Round: {ROUNDS[choice]}\n\n{question_text}',reply_markup=buildResultKeyboard())
    elif choice in CATEGORIES:
        question_text = getQuestionCategory(choice)
        await query.edit_message_text(f'Category: {CATEGORIES[choice]}\n\n{question_text}',reply_markup=buildResultKeyboard())
    else:
        await query.edit_message_text(text=f'Error: Invalid choice. Please try again.',reply_markup=buildResultKeyboard())
    




        
# helper functions
def getQuestionRound(round_):
    chosen_round = round_
    question = None
    if chosen_round:
        ids = pull_id_withRound(con,chosen_round)
        
        if ids:  
            id_number = random.choice(ids)
            question = select_question(con,id_number)
            
    return question[0] if question else None


def getQuestionCategory(category):
    chosen_category  = category
    question = None
    
    if chosen_category:
        ids = pull_id_withCategory(con,chosen_category)
    
        if ids:  
            id_number = random.choice(ids)
            question = select_question(con,id_number)
                
        
    
    return question[0] if question else None


                    
        
