import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from quiz_generator import QuizGenerator
import uvicorn
import uuid

# Initialize FastAPI app
app = FastAPI(title="AI Quiz Generator")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize quiz generator
quiz_generator = None

def get_quiz_generator():
    global quiz_generator
    if quiz_generator is None:
        try:
            quiz_generator = QuizGenerator()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return quiz_generator

# Session data (for simplicity, using in-memory storage - in production use a proper session management)
quiz_sessions = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.route("/generate-quiz", methods=["GET", "POST"])
async def generate_quiz(request: Request):
    if request.method == "POST":
        form_data = await request.form()
        topic = form_data.get("topic")
        difficulty = form_data.get("difficulty")
        
        if not topic or not difficulty:
            return RedirectResponse(url="/")
        
        quiz_generator = get_quiz_generator()
        quiz_data = quiz_generator.generate_quiz(topic, difficulty)
        
        session_id = os.urandom(16).hex()
        quiz_sessions[session_id] = {
            "topic": topic,
            "difficulty": difficulty,
            "questions": quiz_data,
            "current_question": 0,
            "score": 0,
            "answers": []
        }
        
        return RedirectResponse(url=f"/quiz/{session_id}/0", status_code=303)
    else:
        return templates.TemplateResponse("generate_quiz.html", {"request": request})

@app.get("/quiz/{session_id}/{question_index}", response_class=HTMLResponse)
async def show_question(request: Request, session_id: str, question_index: int):
    # Get session data
    session = quiz_sessions.get(session_id)
    if not session:
        return RedirectResponse(url="/", status_code=303)
    
    # Get current question data
    questions = session["questions"]
    if question_index >= len(questions) or question_index < 0:
        return RedirectResponse(url=f"/results/{session_id}", status_code=303)
    
    question_data = questions[question_index]
    total_questions = len(questions)
    
    return templates.TemplateResponse(
        "question.html", 
        {
            "request": request,
            "session_id": session_id,
            "question_index": question_index,
            "question": question_data["question"],
            "options": question_data["options"],
            "total_questions": total_questions,
            "current_question": question_index + 1
        }
    )

@app.post("/submit-answer/{session_id}/{question_index}")
async def submit_answer(
    session_id: str, 
    question_index: int, 
    answer: str = Form(...)
):
    # Get session data
    session = quiz_sessions.get(session_id)
    if not session:
        return RedirectResponse(url="/", status_code=303)
    
    # Save the answer
    current_question = session["questions"][question_index]
    is_correct = answer == current_question["answer"]
    
    session["answers"].append({
        "question_index": question_index,
        "selected_answer": answer,
        "correct_answer": current_question["answer"],
        "is_correct": is_correct
    })
    
    if is_correct:
        session["score"] += 1
    
    # Move to next question or results
    next_question = question_index + 1
    if next_question >= len(session["questions"]):
        return RedirectResponse(url=f"/results/{session_id}", status_code=303)
    else:
        return RedirectResponse(url=f"/quiz/{session_id}/{next_question}", status_code=303)

@app.get("/finish-early/{session_id}")
async def finish_early(session_id: str):
    """
    Handle the request to finish a quiz early.
    Only answered questions are scored, unanswered questions are skipped.
    """
    # Get session data
    session = quiz_sessions.get(session_id)
    if not session:
        return RedirectResponse(url="/", status_code=303)
    
    # Redirect to results page
    return RedirectResponse(url=f"/results/{session_id}", status_code=303)

@app.get("/results/{session_id}", response_class=HTMLResponse)
async def show_results(request: Request, session_id: str):
    # Get session data
    session = quiz_sessions.get(session_id)
    if not session:
        return RedirectResponse(url="/", status_code=303)
    
    # Calculate score
    score = session["score"]
    total = len(session["questions"])
    answered = len(session["answers"])
    percentage = (score / answered) * 100 if answered > 0 else 0
    
    # Get the review data
    review_data = []
    for i, answer_data in enumerate(session["answers"]):
        q_index = answer_data["question_index"]
        question = session["questions"][q_index]
        review_data.append({
            "question": question["question"],
            "selected": answer_data["selected_answer"],
            "correct": answer_data["correct_answer"],
            "is_correct": answer_data["is_correct"]
        })
    
    return templates.TemplateResponse(
        "results.html", 
        {
            "request": request,
            "topic": session["topic"],
            "difficulty": session["difficulty"],
            "score": score,
            "total": total,
            "answered": answered,
            "percentage": percentage,
            "review": review_data,
            "finished_early": answered < total
        }
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
