from telegram import Update
from telegram.ext import ContextTypes
from database import init_db,exact_search,get_all_questions
from huggingface_hub import InferenceClient
import os


SIMILARITY_THRESHOLD = 0.50
con  = init_db()

# Initialize HuggingFace client for semantic search
hf_client = InferenceClient(
    provider="auto",
    api_key=os.environ.get("HF_TOKEN"),
)



async def keywordSearch(update:Update,context:ContextTypes.DEFAULT_TYPE,word):
    dic = {}
    response = exact_search(con,word)
    
    if response:
    
        for question in response:
            question_description  = question[0]
            question_round = question[1]
            question_type = question[2]
            
            if (question_description,question_round,question_type) in dic:
                dic[(question_description,question_round,question_type)]['count'] +=1
            else:
                dic[(question_description,question_round,question_type)]= {'count':1,'score':None}

        

            
    
    return dic
  
    
   
    
# semantic search
async def semanticSearch(update:Update,context:ContextTypes.DEFAULT_TYPE,word):
        dic = {}

        questions = get_all_questions(con)

        if not questions:
            return dic

        # Extract question texts for batch comparison
        question_texts = [q[0] for q in questions]

        # Get similarity scores from HuggingFace API
        try:
            scores = hf_client.sentence_similarity(
                sentence=word,
                other_sentences=question_texts,
                model="sentence-transformers/all-MiniLM-L6-v2",
            )
        except Exception as e:
            # If API fails, return empty dict (keyword search still works)
            return dic

        for i, question in enumerate(questions):
            score = scores[i]
            if score > SIMILARITY_THRESHOLD:
                question_description = question[0]
                question_round = question[1]
                question_type = question[2]

                # saving in a dictionary to track
                if (question_description,question_round,question_type) in dic:
                    dic[(question_description,question_round,question_type)]['count'] +=1
                else:
                    dic[(question_description,question_round,question_type)]= {'count':1, 'score':score}

        return dic

             
async def search(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Please include a question, for example: /search google drive system'
        )
        
        return 
    
 
    word = ' '.join(context.args)   
    
    kw = await keywordSearch(update,context,word)
    sm = await semanticSearch(update,context,word)
    
    merged_dic  = {}

    for k in kw.keys() | sm.keys():
        merged_dic[k] = {
            'count': max(kw.get(k, {}).get('count', 0), sm.get(k, {}).get('count', 0)),
            'score': sm.get(k, {}).get('score'),
        }
 
        
    
    sorted_by_key = dict(sorted(merged_dic.items(),key = lambda item:item[1]['score'] or 0, reverse = True))
    if not sorted_by_key:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='No results found.')
        return
    for key,value in sorted_by_key.items():
        text,round,category = key
        frequency = value['count']
        score = value['score']
        
        if score != None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                # text = 'trial'
                text=f' Description: {text}\n'
                    f'Round: {round}\n'
                    f'Type: {category}\n'
                    f'· Asked {frequency} times\n'  
                    f'similarity: {score:.2f}'  #because I want to do an overall dic and keyword doesn't have score, even if it has it will be different but with the same question
            )
            
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                # text = 'trial'
                text=f' Description: {text}\n'
                    f'Round: {round}\n'
                    f'Type: {category}\n'
                    f'· Asked {frequency} times'  
            )
            
            
        
        