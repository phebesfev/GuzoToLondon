import sqlite3

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

def insert_question(con, text, round_, category, submitted_by):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO questions (text,round,category,submitted_by) VALUES (?,?,?,?)",  
        # -- list the columns you're actually inserting, matching ? count
        (text, round_, category, submitted_by)                                          # the real values, in the same order
    )
    con.commit()

def get_all_questions(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM questions")
    return cur.fetchall()


# async def ()

if __name__ == "__main__":
    con = init_db()
    # insert_question(con, "sample question", "1", "technical", "pheebs")
    for row in get_all_questions(con):
        print(row)
        
        
    # conv_handler = Conver