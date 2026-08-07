import sqlite3
import numpy as np
from constants import ROUNDS,CATEGORIES
def init_db():
    con = sqlite3.connect('guzo.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,                 -- type + PRIMARY KEY
            text TEXT NOT NULL,               -- type + NOT NULL
            round TEXT NOT NULL CHECK (round IN ('phone', '1', '2', '3', 'final')),   -- type, NOT NULL, your finalized value list
            category TEXT CHECK (category IN ('technical','behavioral')),               -- type only — nullable, no NOT NULL
            embedding BLOB,              -- type only — will hold bytes later, NULL for now
            submitted_by INTEGER,           -- type only — nullable
            created_at TEXT DEFAULT CURRENT_TIMESTAMP  -- type + your default value
        )
    """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS related_question (
                    question_id_a INTEGER NOT NULL,
                    question_id_b INTEGER NOT NULL,
                    similarity_score REAL NOT NULL

                )
                 """)
    con.commit()
    return con


def insert_question(con, text, round_, category, embedding, submitted_by):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO questions (text,round,category,embedding,submitted_by) VALUES (?,?,?,?,?)",  
        # -- list the columns you're actually inserting, matching ? count
        (text, round_, category,embedding, submitted_by)                                          # the real values, in the same order
    )
    con.commit()
    return cur.lastrowid
    
    
def insert_related_question(con,question_id_a,question_id_b,similarity_score):
    cur = con.cursor()
    cur.execute("""
                INSERT INTO related_question 
                (question_id_a,question_id_b,similarity_score) 
                VALUES (?,?,?)
                 """,
                 (question_id_a,question_id_b,similarity_score)
                 )
    con.commit()
    
               

def get_all_questions(con):
    cur = con.cursor()
    cur.execute("SELECT text,round,category,embedding FROM questions")
    question = cur.fetchall()
    
    return question


def get_all_related_question(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM related_question")
  
    return cur.fetchall()
    
def get_embedding(con):
    cur = con.cursor()
    cur.execute("""
                SELECT id,embedding 
                FROM questions
                WHERE embedding IS NOT NULL
                 """)
    
    blob = cur.fetchall()
    vec = [None]* (len(blob))
    for i in range(len(blob)):
        vec[i] = (blob[i][0],np.frombuffer(blob[i][1],dtype = np.float32))
        
    return vec



def pull_all_id(con):
    cur  = con.cursor()
    cur.execute(
        """
        SELECT id
        FROM questions
        """    
    )
    all_ids = cur.fetchall()
    all_id = [id[0] for id in all_ids]
        
    return all_id

def pull_id_withRound(con,round):
    cur  = con.cursor()
    cur.execute(
        """
        SELECT id
        FROM questions
        WHERE round = ?
        """ 
        ,(round,)   
    )
    all_ids = cur.fetchall()
    all_id = [id[0] for id in all_ids]
        
    return all_id

def pull_id_withCategory(con,category):
    cur  = con.cursor()
    cur.execute(
        """
        SELECT id
        FROM questions
        WHERE category = ?
        """ 
        ,(category,)   
    )
    all_ids = cur.fetchall()
    all_id = [id[0] for id in all_ids]
        
    return all_id
    

def select_question(con,id_number):
    cur = con.cursor()
    cur.execute(" SELECT text,round,category FROM questions WHERE id  = ?",(id_number,))
    return cur.fetchone()

def exact_search(con,word):
    cur = con.cursor()
    cur.execute("""
                SELECT text,round,category
                FROM questions
                WHERE text LIKE ?
                """,
                (f'%{word}%',))
    response = cur.fetchall()
    return response


def deleteIfEmbeddingisNull(con):
    cur = con.cursor()
    cur.execute(" DELETE  FROM questions WHERE embedding is NULL")
    
  
def getCategory(con):
    cur = con.cursor()
    cur.execute("SELECT category, COUNT(*) FROM questions GROUP BY category;")  
    response = cur.fetchall()
    return response



round_list = ",".join("'" + k.replace("'", "''") + "'" for k in ROUNDS)
cat_list   = ",".join("'" + k.replace("'", "''") + "'" for k in CATEGORIES)


# a code to run migration

def migration(con):
    cur = con.cursor()    
     
    cur.execute(f"""
                CREATE TABLE questions_new (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    round TEXT NOT NULL CHECK (round IN ({round_list})),
                    category TEXT CHECK (category IN ({cat_list})),
                    embedding BLOB,
                    submitted_by INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    cur.execute("""
        INSERT INTO questions_new (id, text, round, category, embedding, submitted_by, created_at)
        SELECT id, text, round, category, embedding, submitted_by, created_at
        FROM questions
    """)
    
    cur.execute("DROP TABLE questions")
    cur.execute("ALTER TABLE questions_new RENAME TO questions")
    
    con.commit()
    
if __name__ == "__main__":
    con = init_db()
    cur  = con.cursor()
    # print(pull_all_id(con))
    # print(select_question(con,11))
    
    # for row in get_all_questions(con):
    #     print(row)

    # for related in get_all_related_question(con):
    #     print(related)
    
    # print(exact_search(con,'bloomberg'))
    # print(deleteIfEmbeddingisNull(con))
    # print(pull_all_id(con))
    # migration(con)
    print(getCategory(con))
    
    
    
    
    
    
    



    
        