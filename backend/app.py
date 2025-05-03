import json
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from utils import db, openai_client

app = Flask(__name__)
CORS(app)  

@app.route('/api/users', methods=['POST'])
def get_user():
    data = request.get_json()
    print(data)
    student_id = data.get('student_id')

    if not student_id:
        return jsonify({'error': "Missing 'id' in request"}), 400 
    
    conn = sqlite3.connect("data/new_sbu.db") 
    cur = conn.cursor()
    student = db.get_student_info(cur, student_id)
    conn.close()

    if student:
        return jsonify(student.to_dict()), 200
    
    return jsonify({'error': "Invalid id"}), 400

@app.route('/api/recommendations', methods=['POST'])
def get_course_recommendations():
    data = request.get_json()
    print(data)
    student_id = data.get('id')

    if not student_id:
        return jsonify({'error': "Missing 'id' in request"}), 400 

    conn = sqlite3.connect("data/new_sbu.db") 
    cur = conn.cursor()

    student = db.get_student_info(cur, student_id)
    courses = db.get_eligible_courses(cur, student_id)
    courses = [course.str2() for course in courses]
    recs = openai_client.get_recommended_courses(courses, student)

    conn.close()

    return jsonify(json.loads(recs)), 200

@app.route('/api/courses/<course_id>', methods=['GET'])
def get_course_reviews(course_id):
    conn = sqlite3.connect("data/new_sbu.db") 
    cur = conn.cursor()

    course = db.get_course_from_db(cur, course_id)

    conn.close()

    if course:
        return jsonify(course.to_dict()), 200
    
    return jsonify({'error': "Invalid course id"}), 400

@app.route('/api/professors/<professorId>/reviews', methods=['GET'])
def get_prof_reviews(professorId):
    pass

@app.route('/api/edit_interests', methods=['POST'])
def edit_interests():
    data = request.get_json()
    print(data)

    student_id = data.get('student_id')
    interests = data.get('interests')

    if not student_id or not interests:
        return jsonify({'error': 'Missing info'}), 400 
    
    conn = sqlite3.connect("data/new_sbu.db") 
    cur = conn.cursor()
    action = db.edit_student_interests(cur, student_id, interests)

    conn.commit()
    conn.close()

    if not action:
        return '', 200
    
    return '', 400

@app.route('/api/add_cc_record', methods=['POST'])
def add_completed_course():
    data = request.get_json()
    print(data)

    student_id = data.get('student_id')
    course_id = data.get('course_id')

    if not student_id or not course_id:
        return jsonify({'error': 'Missing info'}), 400 
    
    conn = sqlite3.connect("data/new_sbu.db") 
    cur = conn.cursor()
    action = db.insert_completed_course(cur, student_id, course_id)

    conn.commit()
    conn.close()

    if not action:
        return '', 200
    
    return '', 400

if __name__ == "__main__":
    app.run(debug=True, port=8000)
