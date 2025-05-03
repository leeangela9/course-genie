from dotenv import load_dotenv
import openai
import os
import textwrap

from utils.objects import Post

load_dotenv()

openai.api_key  = os.getenv('OPENAI_API_KEY')

sysprompt1 = """
    You are a thoughtful and helpful academic advisor.

    Your role is to recommend university courses to students based on their completed coursework, goals, and interests. When making suggestions, consider course prerequisites, difficulty, topic relevance, and logical progression.

    Be concise, supportive, and honest — prioritize clarity and practicality over enthusiasm.
    """

def get_completion(prompt, temperature=0.6, sysprompt=None, model='gpt-4o-mini'):
    """wrapper for openai api call"""
    if sysprompt:
        messages = [
            {'role': 'system', 'content': sysprompt},
            {'role': 'user', 'content': prompt}
        ]
    else:
        messages = [{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message['content']

def get_recommended_courses(courses, student):
    """recommends up to 5 courses for a student based on their interests, career goals, and the course descriptions/summaries."""

    sysprompt = """
        You are a thoughtful and helpful academic advisor.

        Your job is to review a list of courses and recommend the most suitable ones for the student based on their interests, academic history, and career goals.

        Prioritize how well the course content (description + summary) aligns with the student's interests and goals.
        Do not reject a course solely based on a negative sentiment if it aligns well with the student's career direction.

        Recommend a maximum of 5 courses.
    """

    courses = '\n'.join(courses)

    task = textwrap.dedent(f"""
        Consider the student's profile:

        - Major: {student.major}
        - Interests: {student.interests}

        When evaluating course recommendations, pay close attention to whether the sentiment or student feedback is relevant to someone with this major. 
        For example, if a course is poorly reviewed by non-CS majors but well-suited for CS majors, that distinction matters.

        Your task is to recommend up to 5 courses that align well with the student’s academic background and interests. 
        Prioritize interest and career alignment over general sentiment.

        If the sentiment or summary for a course does not seem meaningful to it, feel free to ignore it.

        For each recommended course, include:

        - code: the course code
        - explanation: a brief reason why it's a good fit for the student

        Format your response exactly like this:

        [
        {{
            "code": "CSE320",
            "explanation": "Aligns with the student's interest in systems programming and provides foundational OS-level knowledge..."
        }},
        ...
        ]

        Do not include any extra commentary or explanations outside the list.

        Courses:
        {courses}
    """)


    return get_completion(task, 0.7, sysprompt)

def get_course_sentiment(summaries):
    """generates overall sentiment, followed by reasoning for a specific course"""

    # summaries = get_posts_from_db(course_code)

    # if not summaries:
    #     return None

    formatted_summaries = '\n'.join(summaries)

    task = textwrap.dedent(f"""
        Your task is to provide an overall summary focusing on sentiment, recurring themes, and any controversial ideas.
        Consider aspects such as workload, topics, projects, grades, exams, and professors.

        If the information is insufficient, simply return "Lack of information." Do not fabricate details.

        Use natural phrasing like "Students found this course..." or "Many students appreciated..." 
        Keep your summary clear and concise (limit to 400 characters).

        Return your response strictly in the following JSON format:

        {{
            "sentiment": "positive" | "negative" | "mixed",
            "summary": "Students found the course intellectually engaging but noted that the exams were extremely difficult. While some praised the hands-on projects, others felt the grading was harsh."
        }}

        Do not include any explanation or extra text outside this JSON object.

        Below are the summaries to analyze:
        {formatted_summaries}

        """)

    return get_completion(task)

def summarize_post(post: Post):
    """generates summary for a Reddit post"""

    task = textwrap.dedent(f"""
        Instructions:

        You are provided with the following Reddit post:

        {post}

        Review the comments and summarize anything notable. Focus on aspects such as difficulty, professors, exams, assignments, workload, grades, or the overall course experience.
        
        Try to understand the flow of the conversation and connect related ideas when summarizing. Capture key points that emerge across multiple comments.

        Keep your summary under 200 characters.

        Note any strong emotional language used by students (e.g., "so hard", "bad", "fun", "exciting", "doable").
        Also highlight any comments that mention how the course connects to specific careers or industries (e.g., useful for web development, data science, etc.).

        Format your response exactly like this:

        {{
            "summary": "Your summary here"
        }}

        Do not include any extra text outside the JSON structure.
    """)
    
    return get_completion(task)

if __name__ == '__main__':
    pass