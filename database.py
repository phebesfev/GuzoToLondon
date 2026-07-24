import sqlite3
import numpy as np

def init_db():
    con = sqlite3.connect('guzo.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,                 -- type + PRIMARY KEY
            text TEXT NOT NULL,               -- type + NOT NULL
            round TEXT NOT NULL CHECK (round IN ('1', '2', 'system design', 'behavioral', 'final')),   -- type, NOT NULL, your finalized value list
            category TEXT,               -- type only — nullable, no NOT NULL
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
    cur.execute("SELECT text,round FROM questions")
    return cur.fetchall()


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
        print(vec[0])
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
    

def select_question(con,id_number):
    cur = con.cursor()
    cur.execute(" SELECT text FROM questions WHERE id  = ?",(id_number,))

    question = cur.fetchone()
    return question[0]
    
    
if __name__ == "__main__":
    con = init_db()
    cur  = con.cursor()
    print(pull_all_id(con))
    print(select_question(con,11))
    
    for row in get_all_questions(con):
        print(row)

    # for related in get_all_related_question(con):
    #     print(related)
        