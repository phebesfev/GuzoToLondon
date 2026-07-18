from sentence_transformers import SentenceTransformer
import numpy as np
from database import get_all_questions,init_db,insert_related_question
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


con=init_db()
def toVector(sentence):
    embedding = model.encode(sentence)
    return embedding
 
   
# embdding1 = toVector(["I love my cat","hating on dogs","do you really love me?"]) 



blob = get_all_questions(con)
    
def cosineSimilarity(curr_vector,blob):
    similarity = model.similarity(curr_vector,blob)
    return  float(similarity)
           
            
  
            
    
    
    
    
