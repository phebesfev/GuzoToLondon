from telegram import Update
from telegram.ext import ContextTypes
from database import init_db,exact_search,get_all_questions
from embedding import toVector,cosineSimilarity,toFloat


SIMILARITY_THRESHOLD = 0.50
con  = init_db()



async def keywordSearch(update:Update,context:ContextTypes.DEFAULT_TYPE,dic):
    
    if context.args:
        word = ' '.join(context.args)   
        response = exact_search(con,word)
        
        if response:
        
            for question in response:
                question_description  = question[0]
                question_round = question[1]
                question_type = question[2]
                
                if (question_description,question_round,question_type) in dic:
                    dic[(question_description,question_round,question_type)] +=1
                else:
                    dic[(question_description,question_round,question_type)] = 1
            
              
            # sorted_by_key = dict(sorted(dic.items(),reverse=True))
            # for key,value in sorted_by_key.items():
            #     text,round,category = key
            #     frequency = value
            #     #score = round(score,2) #rounding for 2 round places to make it readable
                
            #     await context.bot.send_message(
            #         chat_id=update.effective_chat.id,
            #         # text = 'trial'
            #         text=f' Description: {text}\n'
            #             f'Round: {round}\n'
            #             f'Type: {category}\n'
            #             f'· Asked {frequency} times'  
            #     )
        
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
        
    return True
   
    
# semantic search
async def semanticSearch(update:Update,context:ContextTypes.DEFAULT_TYPE,dic):
    
    
    if context.args:
        word = ' '.join(context.args)        
        embedding = toVector(word)
        questions = get_all_questions(con)
        
        for question in questions:
            if question[3]:
                embedding_new = toFloat(question[3])
                score = cosineSimilarity(embedding,embedding_new)
                if score > SIMILARITY_THRESHOLD:
                    
                    question_description  = question[0]
                    question_round = question[1]
                    question_type = question[2]
                    
                    
                    # saving in a dictionary to track
                    if (question_description,question_round,question_type) in dic:
                        dic[(question_description,question_round,question_type)] +=1
                    else:
                        dic[(question_description,question_round,question_type)] = 1
                
        sorted_by_key = dict(sorted(dic.items(),reverse=True))
        for key,value in sorted_by_key.items():
            text,round,category = key
            frequency = value
            #score = round(score,2) #rounding for 2 round places to make it readable
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                # text = 'trial'
                text=f' Description: {text}\n'
                    f'Round: {round}\n'
                    f'Type: {category}\n'
                    f'· Asked {frequency} times'  
                    # removed similarity: {score} because I want to do an overall dic and keyword doesn't have score, even if it has it will be different but with the same question
            )
                    
    else:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Please include a question, for example: /search google drive system'
            )
                    
                    
    # putting them in a dictionary with score,text,round,:frequency and then seinding it with the limits

             
async def search(update:Update,context:ContextTypes.DEFAULT_TYPE):
    dic = {}
    firstSearch = await keywordSearch(update,context,dic)
    if firstSearch:
        await semanticSearch(update,context,dic)