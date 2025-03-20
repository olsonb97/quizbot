# QuizBot 🤖

**DISCLAIMER**: THIS WAS MOSTLY VIBE CODED BY CLAUDE 3.7. I MADE THIS FOR MY OWN PERSONAL
LEARNING, BUT AM SHARING IT IN CASE IT HELPS SOMEONE ELSE. USE AT YOUR OWN WILL.

A web application that generates custom quizzes on any topic using the OpenAI API (GPT-4o).

## Features

- Choose a topic
- Choose difficulty level (Easy, Medium, Hard)
- 10 AI-generated questions adapt to the chosen difficulty

## Requirements

- Python 3.8+
- OpenAI API Key

## Installation

1. Clone the repository


2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key as an environment variable:
   
   Windows:
   -  ```
      set OPENAI_API_KEY=your_api_key_here
      ```
   - Or add to your system environment variables for persistence
   
   macOS/Linux:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

## Running the Web App

1. Start the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

3. Enter a topic, select a difficulty level, and generate your quiz!

## How It Works

The application uses OpenAI's API to generate custom quiz questions based on your specified topic and difficulty level. The AI adapts the complexity of questions according to the selected difficulty:

- **Easy**: Basic knowledge and simple recall questions
- **Medium**: Application of concepts and moderate complexity
- **Hard**: Complex, analytical questions that require deep understanding

## Tech Stack

- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- AI Integration: OpenAI API
- Templates: Jinja2

**Note**: You must pay for OpenAI API usage