from telegram import Update
from telegram.ext import ContextTypes
from database import init_db,exact_search,get_all_questions,get_embedding
from embedding import toVector,cosineSimilarity,toFloat

SIMILARITY_THRESHOLD = 0.50
con  = init_db()
async def keywordSearch(update:Update,context:ContextTypes.DEFAULT_TYPE):
    # searching using sql
    if context.args:
        word = context.args[0]
        
      
            
        response = exact_search(con,word)
        
        if response:
        
            for question in response:
                print(question)
                question_description  = question[0]
                question_round = question[1]
                question_type = question[2]
            
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f' Description: {question_description}\n'
                        f'Round: {question_round}\n'
                        f'Type: {question_type}'  
                )
        
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='No question matches your query, please search another question'
            )
            
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Please include a question, for example: /search google drive system'
            )
        

# semantic search
async def semanticSearch(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if context.args:
        word = ' '.join(context.args)
        
        embedding = toVector(word)
        # print('word embedding',embedding)
        questions = get_all_questions(con)
        
        for question in questions:
            if question[3]:
                embedding_new = toFloat(question[3])
                x = cosineSimilarity(embedding,embedding_new)
                if x > SIMILARITY_THRESHOLD:
                    
                    question_description  = question[0]
                    question_round = question[1]
                    question_type = question[2]
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        # text = 'trial'
                        text=f' Description: {question_description}\n'
                            f'Round: {question_round}\n'
                            f'Type: {question_type}'  
                    )
                    
    else:
            await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Please include a question, for example: /search google drive system'
                )
                    

                
                