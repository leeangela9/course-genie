import json
from dotenv import load_dotenv
import os
import praw
from utils.db import get_eligible_courses, get_uncompleted_courses, insert_course_sentiment, insert_post
from utils.openai_client import get_course_sentiment, get_recommended_courses, summarize_post
from utils.models import Post, Comment, Student, Course
import sqlite3

load_dotenv()

# secrets
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

# developer credentials
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def get_replies(cmts, comment, limit=10, i=1):
    """helper to recursively get comments"""

    if i > limit:
        return
    
    for reply in comment.replies:
        text = reply.body.strip().replace('\n', ' ')
        if text and text != '[deleted]' and text != '[removed]':
            cmts.append(Comment(reply.id, text, reply.score))
            get_replies(cmts, reply, limit, i+1)

def get_posts(course_code):
    """gets relevant posts to specified course"""

    query = f"{course_code} OR {course_code[:3]} {course_code[3:]}"
    submissions = reddit.subreddit("SBU").search(query, sort='relevant', time_filter='all', limit=15)
    submissions = sorted(submissions, key=lambda s: s.score, reverse=True)

    posts = []

    for i, submission in enumerate(submissions):

        # expand existing comment tree to obtain more cmts
        submission.comments.replace_more(limit=10)
        comments = submission.comments.list()
        # might yield overlapping comments again
        comments = list({comment.id: comment for comment in comments}.values())
        comments = sorted(comments, key=lambda c: c.score, reverse=True)

        if not comments:
            continue
        
        context = submission.selftext.replace('\n', ' ')

        cmts = []
        for cmt in comments:
            if cmt.body and cmt.body.strip() != '[deleted]' and cmt.body.strip() != '[removed]':
                cmts.append(Comment(cmt.id, cmt.body.strip().replace('\n', ' '), cmt.score))
                get_replies(cmts, cmt)

        cmts = list({c.id: c for c in cmts}.values())
        post = Post(submission.id, submission.title, context, submission.score, course_code, cmts)
        posts.append(post)

    return posts

def test_insert_sentiments():

    conn = sqlite3.connect("data/new_sbu.db") # if cd is backend
    cur = conn.cursor()

    cur.execute("SELECT course_code FROM courses")
    courses = cur.fetchall()
    courses = [item[0] for item in courses]

    for course in courses[1:]:
        summaries = []

        posts = get_posts(course)

        for post in posts:
            try:
                res = summarize_post(posts[0], )
                res = json.loads(res)
                post.summary = res.get('summary')
                insert_post(cur, post)

                summaries.append(res.get('summary'))

            except Exception as e:
                print("Error1:", e)

        if len(summaries) > 3:
            try:
                res = get_course_sentiment(summaries)
                res = json.loads(res)

                sentiment = res.get('sentiment')
                summary = res.get('summary')

                insert_course_sentiment(cur, course, sentiment, summary)

            except Exception as e:
                print("Error2:", e)

        else:
            print('not enough info for {course}')
            continue

        print(course)

    conn.commit()
    conn.close()

def test_get_recs():
    conn = sqlite3.connect("data/new_sbu.db") # if cd is backend
    cur = conn.cursor()

    cur.connection.row_factory = sqlite3.Row

    # courses = get_eligible_courses(cur, 1)
    courses = get_uncompleted_courses(cur, 1)
    courses = [Course(c[0], c[1], c[2], c[3], None, c[4], c[5]).str2() for c in courses]

    angela = Student(1, 'Angela', 'Computer Science (CSE)', 'neural networks, web development')

    recs = get_recommended_courses(courses, angela)
    recs = json.loads(recs) # list of dicts

    print(recs)

    conn.close()

def test_insert_ams_sentiments():

    conn = sqlite3.connect("data/new_sbu.db") # if cd is backend
    cur = conn.cursor()

    cur.execute("SELECT course_code FROM courses WHERE course_code LIKE 'AMS%'")
    courses = cur.fetchall()
    courses = [item[0] for item in courses]

    for course in courses[1:]:
        summaries = []

        posts = get_posts(course)

        for post in posts:
            try:
                res = summarize_post(posts[0], )
                res = json.loads(res)
                post.summary = res.get('summary')
                insert_post(cur, post)

                summaries.append(res.get('summary'))

            except Exception as e:
                print("Error1:", e)

        if len(summaries) > 3:
            try:
                res = get_course_sentiment(summaries)
                res = json.loads(res)

                sentiment = res.get('sentiment')
                summary = res.get('summary')

                insert_course_sentiment(cur, course, sentiment, summary)

            except Exception as e:
                print("Error2:", e)

        else:
            print('not enough info for {course}')
            continue

        print(course)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # test_insert_ams_sentiments()
    pass
