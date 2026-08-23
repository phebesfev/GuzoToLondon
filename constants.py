from telegram import InlineKeyboardButton,InlineKeyboardMarkup

ROUNDS = {
    'phone': '📞 Phone Screen',
    '1':     '1️⃣ Round 1',
    '2':     '2️⃣ Round 2',
    '3':     '🏗 Round 3 / System Design',
    'final': '🏁 Final — EM/HR',
}
CATEGORIES = {
    'technical':  '💻 Technical',
    'behavioral': '🧠 Behavioral',
}


def buildInlineKeyboard(options,prefix):
    buttons = [ InlineKeyboardButton(value,callback_data =f'{prefix}:{key}') 
               for key,value in options.items()
    ]
    
    row = [buttons[i:i+2] for i in range(0,len(buttons),2)]
    return InlineKeyboardMarkup(row)


def buildResultKeyboard():
    keyboard = [
        [InlineKeyboardButton('another question', callback_data='anotherquestion')],
        [InlineKeyboardButton('🔄 another filter', callback_data='back'),
        InlineKeyboardButton('✅ done',callback_data='done')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)