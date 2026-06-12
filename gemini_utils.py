import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_text(prompt: str):
    """Generate text using official Gemini SDK"""
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not set in environment")
    
    try:
        # Configure the API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Use the most reliable and fast models from your available list
        model_names = [
            'models/gemini-2.0-flash-001',      # Stable Flash model
            'models/gemini-2.5-flash',          # Latest Flash model
            'models/gemini-pro-latest',         # Stable Pro model
            'models/gemini-2.5-pro',            # Latest Pro model
        ]
        
        for model_name in model_names:
            try:
                print(f"🔗 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=2048,
                    )
                )
                
                if response.text:
                    print(f"✅ Success with model: {model_name}")
                    return response.text
                else:
                    print(f"⚠️ No text generated with {model_name}")
                    continue
                    
            except Exception as e:
                print(f"❌ Failed with {model_name}: {e}")
                continue
                
        raise Exception("All model attempts failed")
            
    except Exception as e:
        print(f"❌ Final error: {e}")
        raise Exception(f"Gemini API failed: {str(e)}")

def generate_course_content(topic: str):
    """Generate structured course with modules and lessons"""
    prompt = f"""
    Create a detailed 3-module beginner-friendly course on the topic: {topic}.
    
    FORMAT REQUIREMENTS:
    - Use exactly this format for each module:
    
    Module 1: [Module Title]
    Description: [Clear, engaging description of what this module covers]
    Lesson 1.1: [Lesson Title]
    Content: [Detailed explanation of the lesson content with practical examples]
    Lesson 1.2: [Lesson Title] 
    Content: [Detailed explanation of the lesson content with practical examples]
    
    Module 2: [Module Title]
    Description: [Clear, engaging description]
    Lesson 2.1: [Lesson Title]
    Content: [Detailed explanation with examples]
    Lesson 2.2: [Lesson Title]
    Content: [Detailed explanation with examples]
    
    Module 3: [Module Title]
    Description: [Clear, engaging description]
    Lesson 3.1: [Lesson Title]
    Content: [Detailed explanation with examples]
    Lesson 3.2: [Lesson Title]
    Content: [Detailed explanation with examples]
    
    Make sure each module builds upon the previous one and the content is practical and engaging for beginners.
    """
    return generate_text(prompt)

def generate_module_detail(module_title: str, course_topic: str):
    """Generate deep content for a single module"""
    prompt = f"""
    Write a comprehensive, beginner-friendly lesson for the module "{module_title}" in a course about "{course_topic}".
    
    Include:
    1. A clear introduction to the topic
    2. 4-6 detailed paragraphs explaining the core concepts
    3. 2-3 practical examples with code or real-world applications
    4. One small practice exercise for the learner
    5. A summary of key takeaways
    
    Format the response in clear Markdown with proper headings and code blocks where appropriate.
    Make the content engaging and easy to follow for someone new to {course_topic}.
    """
    return generate_text(prompt)

def generate_embeddings(text):
    """Generate embeddings for text - placeholder implementation"""
    print("⚠️ Embedding generation: Using placeholder")
    return [0.1] * 384

def generate_quiz_prompt(module_title, module_content, num_questions=5):
    return f"""
Create {num_questions} multiple-choice questions (4 options each) for learners about the module:
Title: {module_title}

Content:
{module_content}

Output format (strict JSON):
{{
 "title": "Quiz for {module_title}",
 "questions": [
   {{
     "question": "<question text>",
     "options": [
       {{"text": "option A", "correct": false}},
       {{"text": "option B", "correct": false}},
       {{"text": "option C", "correct": true}},
       {{"text": "option D", "correct": false}}
     ],
     "explanation": "<short explanation>"
   }},
   ...
 ]
}}
"""
