from telegram.ext import ContextTypes
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup


async def round(update:Update,context:ContextTypes.DEFAULT_TYPE):
    # callback_data is a one that will be sent, and the invisble part of that will be sent 
    keyboard = [
        [
         InlineKeyboardButton('round 1',callback_data='1'),
         InlineKeyboardButton('round 2',callback_data='2')
         ],
        
        [
        InlineKeyboardButton('system design',callback_data='system design'),
        InlineKeyboardButton('behavioral',callback_data='behavioural')
        ],
        
        [
        InlineKeyboardButton('final round',callback_data='final'),
        ],

    ]
    # changing to a format telegram understands
    markup =InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('please choose one round',reply_markup=markup)
    
    
async def button(update:Update,context:ContextTypes.DEFAULT_TYPE) :
    query = update.callback_query
    await query.answer() 
    await query.edit_message_text(text=f'you selected round:{query.data} option')

