import sqlite3
from utils.objects import Course, Post, Student

def get_eligible_courses(cur, student_id):
    """returns courses student can take next (all prerequisites completed, not already taken)"""

    cur.execute("""
        SELECT c.course_code, c.course_name, c.description, c.num_credits, c.overall_sentiment, c.sentiment_summary
        FROM courses c
        WHERE NOT EXISTS (
            SELECT 1
            FROM (
                SELECT req_num
                FROM prerequisites p
                WHERE p.course_id = c.course_code
                GROUP BY req_num
                HAVING SUM(
                    prereq_id IN (
                        SELECT cc.course_id
                        FROM completed_courses cc
                        WHERE cc.student_id = ?
                    )
                ) = 0
            )
        )
        AND c.course_code NOT IN (
            SELECT cc.course_id
            FROM completed_courses cc
            WHERE cc.student_id = ?
        );

    """, (student_id, student_id))

    courses = cur.fetchall()
    for course in courses:
        print(course[0])

    return [Course(course[0], course[1],  course[2],  course[3], None, course[4], course[5]) for course in courses]

def get_uncompleted_courses(cur, student_id):
    """returns all courses the student hasn’t completed — regardless of whether they meet prerequisites"""

    cur.execute("""
        SELECT c.course_code, c.course_name, c.description, c.num_credits, c.overall_sentiment, c.sentiment_summary
        FROM courses c
        WHERE c.course_code IN 
        (
            SELECT a.course_code
            FROM courses a
            EXCEPT
            SELECT cc.course_id
            FROM completed_courses cc
            WHERE cc.student_id = ? 
        );
    """, (student_id, ))

    courses = cur.fetchall()

    # return [Course(course) for course in courses]
    return courses

def insert_course(cur, course: Course):
    """inserts a course into the db if it's not already present"""
    try:
        cur.execute("INSERT OR IGNORE INTO courses(course_code, course_name, description, num_credits) VALUES (?,?,?,?)", (course.code, course.name, course.description, course.credits))
        return 0
    except Exception as _:
        return 1
    
def insert_completed_course(cur, student_id, course_id):
    """inserts a completed course record for a student if it doesn't already exist"""
    cur.execute("INSERT OR IGNORE INTO completed_courses(student_id, course_id) VALUES (?,?)", (student_id, course_id))

def insert_post(cur, post: Post):
    """inserts a post related to a course if it doesn't already exist"""

    cur.execute("INSERT OR IGNORE INTO posts(post_id, course_id, summary) VALUES (?,?,?)", (post.id, post.course, post.summary))

def get_posts_from_db(cur, course_id):
    """gets all posts associated to specified course"""
    cur.execute("SELECT summary, upvotes FROM posts WHERE course_id = ?", (course_id,))
    return cur.fetchall()

def insert_course_sentiment(cur, course_id, sentiment, summary):
    """inserts sentiment/summary associated with specific course"""
    cur.execute("UPDATE courses SET overall_sentiment = ?, sentiment_summary = ? WHERE course_code = ?", (sentiment, summary, course_id))

def insert_prereq(cur, course_id, prereq_id, i):
    """inserts a prerequisite into associated course"""
    # i = the i-th prereq of course
    cur.execute("INSERT OR IGNORE INTO prerequisites(course_id, prereq_id, req_num) VALUES (?,?,?)", (course_id, prereq_id, i))

def insert_student(cur, student: Student):
    """inserts a student record into db"""
    cur.execute("INSERT OR IGNORE INTO students(student_id, name, major, interests) VALUES (?,?,?,?)", (student.id, student.name, student.major, student.interests))

def get_student_info(cur, student_id):
    cur.execute("SELECT student_id, name, major, interests FROM students WHERE student_id = ?", (student_id,))
    student = cur.fetchone()
    return Student(*student) if student else None

def get_course_from_db(cur, course_id):
    cur.execute("SELECT course_code, course_name, description, num_credits, overall_sentiment, sentiment_summary FROM courses WHERE course_code = ?", (course_id,))
    course = cur.fetchone()
    return Course(course[0], course[1],  course[2],  course[3], None, course[4], course[5]) if course else None

def edit_student_interests(cur, student_id, interests):
    try:
        cur.execute("UPDATE students SET interests = ? WHERE student_id = ?", (interests, student_id))
        return 0
    except Exception as _:
        return 1

if __name__ == '__main__':
    conn = sqlite3.connect("data/new_sbu.db") # if cd is backend
    cur = conn.cursor() 
    print(get_student_info(cur, 1))
    conn.close()