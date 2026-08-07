import numpy as np
import os
from dotenv import load_dotenv
import httpx

load_dotenv()
hf_token = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"


def toVector(sentence):
    response = httpx.post(
        API_URL,
        headers={'Authorization':f"Bearer {hf_token}"},
        json={"inputs":sentence},
        timeout=30,
        
    )
    return np.array(response.json()[0],dtype=np.float32)


    
def cosineSimilarity(curr_vector,blob):
    # similarity = model.similarity(curr_vector,blob)
    # return  float(similarity)
    curr_vector = np.array(curr_vector,dtype=np.float32)
    blob = np.array(blob,dtype=np.float32)
    return float(np.dot(curr_vector,blob)/ (np.linalg.norm(curr_vector) *np.linalg.norm(blob)))
           
     
def toFloat(vector):
    to_float = np.frombuffer(vector,dtype = np.float32)

    return to_float       
  
            
    
    
    
    
