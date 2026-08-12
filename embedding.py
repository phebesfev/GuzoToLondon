import numpy as np
import httpx,asyncio
import os
from dotenv import load_dotenv
load_dotenv()

async def toVector(sentence):
    
    url = "https://api.jina.ai/v1/embeddings"
    
    JINA_TOKEN = os.environ.get("JINA_TOKEN")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINA_TOKEN}'
    }
    
    payload = {
    "model": "jina-embeddings-v5-text-small",
    "task": "retrieval.query",
    "normalized": True,
    "input": [
        f'{sentence}'
    ]
    }
    async with httpx.AsyncClient() as client:
        try:
            response= await client.post(url,json=payload,headers=headers)
            response.raise_for_status()
            
            data = response.json()
            word_embeddings =data['data'][0]['embedding']
            
            # print(word_embeddings)
            return np.array(word_embeddings,dtype=np.float32)
            
        except httpx.HTTPStatusError as error:
            print(f'error{error}')
    
def cosineSimilarity(curr_vector,blob):
    
    # change blob to vector
    newVector = toFloat(blob)
    # Formula: dot(a, b) / (norm(a) * norm(b))
    similarity = np.dot(curr_vector,newVector)/(np.linalg.norm(curr_vector)*np.linalg.norm(newVector))
    
    return  float(similarity)
           
     
def toFloat(vector):
    to_float = np.frombuffer(vector,dtype = np.float32)
    return to_float  

print(cosineSimilarity(asyncio.run(toVector('hi')),asyncio.run(toVector('hello'))))  
  
  
            
    
    
    
    
