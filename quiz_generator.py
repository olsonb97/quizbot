import os
import openai
import json

class QuizGenerator:
    def __init__(self):
        # Get the OpenAI API key from environment variables
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_quiz(self, topic, difficulty):
        """
        Generate a quiz on a given topic with specified difficulty.
        
        Args:
            topic (str): The subject to create a quiz about
            difficulty (str): 'easy', 'medium', or 'hard'
        
        Returns:
            list: A list of dictionaries containing questions, options, and answers
        """
        # Create prompt based on difficulty
        system_prompt = f"""
        You are an expert quiz creator. Create a 10-question quiz about {topic}.
        
        The quiz MUST be at {difficulty.upper()} difficulty level. This is extremely important.
        THIS IS NOT FOR FUN. THIS IS FOR EDUCATION. TAKE IT VERY SERIOUSLY.
        
        For each difficulty level, follow these STRICT guidelines:
        
        EASY difficulty:
        - Basic knowledge and simple recall questions
        - Focus on definitions, simple facts, and straightforward concepts
        - Questions should be answerable by someone with minimal knowledge of the topic
        - Use simple vocabulary and direct questions
        - Example: "What is the capital of France?" or "What is HTML used for?"
        
        MEDIUM difficulty:
        - Application of concepts and moderate complexity
        - Questions should require some understanding beyond basic facts
        - May involve making connections between related concepts
        - Can include scenario-based questions that aren't too complex
        - Example: "Which of these elements is NOT typically found in a database schema?" or "How would CSS Flexbox help in the following layout scenario?"
        
        HARD difficulty:
        - Longer form questions that exercise deep knowledge and critical thinking
        - Complex analytical questions that require deep understanding
        - May involve problem-solving, edge cases, or advanced topics
        - Questions should challenge even those familiar with the subject
        - Can include multi-step reasoning, complex scenarios, or detailed technical questions
        - Example: "Given this code snippet with a recursion error, which of these changes would fix the issue?" or "Which algorithm would be most efficient for solving this specific problem and why?"
        
        The difficulty level is {difficulty.upper()}, so all 10 questions MUST adhere to the {difficulty.upper()} guidelines above.
        
        Format your response as a JSON array with 10 items. Each item should have:
        1. "question": The question text
        2. "options": An array of 4 possible answers
        3. "answer": The correct answer (must be one of the options)
        
        Make sure the JSON is valid and properly formatted.
        """
        print(system_prompt) # Debugging
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a {difficulty} quiz about {topic}. Remember, this MUST be {difficulty} difficulty level."}
                ],
                temperature=0.9,
                max_tokens=10000
            )
            
            # Extract and parse the JSON response
            content = response.choices[0].message.content
            
            # Find JSON content - sometimes the AI includes explanatory text
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > 0:
                json_content = content[start_idx:end_idx]
                quiz_data = json.loads(json_content)
                return quiz_data
            else:
                # Try to parse the entire response as JSON
                try:
                    quiz_data = json.loads(content)
                    return quiz_data
                except:
                    raise ValueError("Failed to extract JSON from API response")
                    
        except Exception as e:
            print(f"Error generating quiz: {e}")
            # Return a basic error quiz in the right format
            return [{"question": "Error creating quiz. Please try again.",
                    "options": ["Try again", "Check API key", "Choose another topic", "Contact support"],
                    "answer": "Try again"}]
