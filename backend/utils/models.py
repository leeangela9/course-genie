from typing import List, Optional

class Comment():
    def __init__(self, id, text, upvotes):
        self.id = id
        self.text = text
        self.upvotes = upvotes
        # post_id

    def __str__(self):
        return f"{self.text}"

class Post():
    def __init__(self, id, title, body, upvotes, course, comments: Comment = [], summary = None):
        self.id = id
        self.title = title
        self.body = body
        self.upvotes = upvotes
        self.course = course
        self.comments = comments
        self.summary = summary

    def __str__(self):
        post_str = f"Post: {self.title}\n"
        post_str += f"Context: {self.body}\n"
        if self.summary:
            post_str += f"\nSummary: {self.summary}\n"
        post_str += "\nComments:\n"
        if self.comments:
            for comment in self.comments:
                post_str += f"  - {str(comment)}\n"
        # else:
        #     post_str += "  No comments\n"
        return post_str

class Course():
    def __init__(self, code, name, description, credits, prerequisites = None, sentiment = None, summary = None):
        # Optional[List["Course"]] = None
        self.code = code
        self.name = name
        self.description = description
        self.credits = credits
        self.prerequisites = prerequisites
        self.sentiment = sentiment
        self.summary = summary
    
    # based on interests
    def __str__(self):
        # if not self.prerequisites:
        #     prereq_str = "None"
        # else:
        #     prereq_str = '; '.join(' or '.join(group) for group in self.prerequisites)

        return (
            f"{self.code}: {self.name} ({self.credits} credits)\n"
            f"Description: {self.description}\n"
            f"Prerequisites: {self.prerequisites}\n"
            f"Sentiment: {self.sentiment}\n"
            f"Summary: {self.summary}"
        )
    
    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "credits": self.credits,
            "sentiment": self.sentiment,
            "summary": self.summary
        }

    # based on interests and completed courses
    def str2(self):
        return (
            f"{self.code}: {self.name} ({self.credits} credits)\n"
            f"Description: {self.description}\n"
            f"Sentiment: {self.sentiment}\n"
            f"Summary: {self.summary}"
        )

class Major():
    def __init__(self, code, courses: Course = []):
        self.code = code
        self.courses = courses

    def __str__(self):
        s = ""
        if self.courses:
            s += f"{self.code} Courses:\n"
            for course in self.courses:
                s += f"{str(course)}\n"
        else:
            s += "  No courses listed.\n"
        return s

class Student():
    def __init__(self, id, name, major, interests = None, cmts = None):
        self.id = id
        self.name = name
        self.major = major
        self.interests = interests
        self.cmts = cmts # additional comments to better query

    def __str__(self):
        return  (
            f'[{self.id }] {self.name}\n'
            f'Major: {self.major}\n'
            f'Interests: {self.interests}'
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'major': self.major,
            'interests': self.interests
        }

    
