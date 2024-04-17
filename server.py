from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for
import datetime

app = Flask(__name__)

user_activities = {}

lessons = {
    "1":{
        "lesson_id": "1",
        "title": "Basic Table Setting", 
        "text": "Click an item to learn more",
        "image": "basic_table.png",
        "next_lesson": "2"
    }, 
    "2":{
        "lesson_id": "2",
        "title": "Casual Table Setting", 
        "text": "Click an item to learn more",
        "image": "casual_table.png",
        "next_lesson": "3"
    },
    "3":{
        "lesson_id": "3",
        "title": "Formal Table Setting", 
        "text": "Click an item to learn more",
        "image": "formal_table.png",
        "next_lesson": "end"
    }     
}

quiz_questions = {
    "1": {
        "quiz_id": "1", 
        "question": "In formal table setting, where is the bread plate located?",
        "options": {
            "A": "to the right of the charger",
            "B": "directly above the charger",
            "C": "To the top left of the charger",
            "D": "Below the charger"
        },
        "correct_answer": "C",
        "next_question": "2"
    }, 
    "2": {
        "quiz_id": "2", 
        "question": "Drag and drop the items to practice setting casual table.",
        "next_question": "end"
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/learn/<lesson_id>')
def learn(lesson_id):
    print("Requested lesson_id:", lesson_id)
    lesson = lessons.get(lesson_id)
    print("Lesson:", lesson)
    
    user_id = request.cookies.get('user_id')
    if not lesson:
        return "Lesson not found", 404

    if user_id:
        activity = {
            'type': 'learn',
            'lesson_id': lesson_id,
            'timestamp': datetime.datetime.now().isoformat()
        }
        user_activities.setdefault(user_id, []).append(activity)

    return render_template('learn.html', lesson=lesson)

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    question = quiz_questions.get(quiz_id)
    if not question:
        return "Question not found", 404

    if request.method == 'POST':
        user_answer = request.form['quiz_option']
        correct_answer = question['correct_answer']

        if user_answer == correct_answer:
            feedback = "Correct! Well done."
        else:
            feedback = "Incorrect. Try again!"

        return redirect(url_for('feedback', quiz_id=quiz_id, feedback=feedback))

    return render_template('quiz.html', question=question)

@app.route('/feedback/<quiz_id>')
def feedback(quiz_id):
    feedback = request.args.get('feedback', 'No feedback provided')
    question = quiz_questions.get(quiz_id)
    if not question:
        return "Question not found", 404

    return render_template('feedback.html', feedback=feedback, quiz_id=quiz_id, question=question)

if __name__ == '__main__':
   app.run(debug = True)