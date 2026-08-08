from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def toVector(sentence):
    embedding = model.encode(sentence)
    return embedding

def cosineSimilarity(curr_vector, blob):
    similarity = model.similarity(curr_vector, blob)
    return float(similarity)

def toFloat(vector):
    to_float = np.frombuffer(vector, dtype=np.float32)
    return to_float


    
# def cosineSimilarity(curr_vector,blob):
#     # similarity = model.similarity(curr_vector,blob)
#     # return  float(similarity)
#     curr_vector = np.array(curr_vector,dtype=np.float32)
#     blob = np.array(blob,dtype=np.float32)
#     return float(np.dot(curr_vector,blob)/ (np.linalg.norm(curr_vector) *np.linalg.norm(blob)))
           
     
# def toFloat(vector):
#     to_float = np.frombuffer(vector,dtype = np.float32)

#     return to_float       
  
            
    
    
    
    
