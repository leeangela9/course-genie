import sqlite3

def init_db():
    """initializes database with relevant tables"""
    print("initializing database...")

    conn = sqlite3.connect("data/new_sbu.db") # if im cd backend
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            major VARCHAR(3),
            interests TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_code VARCHAR(6) NOT NULL PRIMARY KEY,  
            course_name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            num_credits SMALLINT NOT NULL,
            overall_sentiment VARCHAR(255),
            sentiment_summary TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS prerequisites (
            course_id VARCHAR(6),
            prereq_id VARCHAR(6),
            req_num INTEGER,
            PRIMARY KEY (course_id, prereq_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (prereq_id) REFERENCES courses (course_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            CHECK (course_id <> prereq_id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS completed_courses (
            student_id INTEGER,
            course_id VARCHAR(6),
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES users (student_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses (course_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id TEXT,
            course_id VARCHAR(6),
            summary TEXT,  
            PRIMARY KEY (post_id, course_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)

    conn.commit()
    conn.close()

    print("initialization completed")

# def test():
#     conn = sqlite3.connect("data/new_sbu.db")
#     cur = conn.cursor()

#     cur.connection.row_factory = sqlite3.Row

#     user = {'name': 'angela', 'major': 'CSE', 'id': 1, 'interests': 'data science, artifical intelligence, web development'}

#     c = get_possible_courses(cur, conn,  user)
    
#     conn.close()
    
#     keys_to_omit = ['antirequisites', 'num_credits', 'min_standing', 'prerequisites']
#     c = [{key: value for key, value in d.items() if key not in keys_to_omit} for d in c]

#     res = get_recommendations(user, c)

if __name__ == "__main__":
    init_db()
    # test()

