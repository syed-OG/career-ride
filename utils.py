import json
import os
import re
from datetime import datetime
import requests
from werkzeug.security import generate_password_hash

def get_career_match_score(user_skills, career_path_skills):
    """Calculate how well a user's skills match a career path's required skills."""
    if not user_skills or not career_path_skills:
        return 0
    
    user_skills_list = [skill.strip().lower() for skill in user_skills.split(',')]
    career_skills_list = [skill.strip().lower() for skill in career_path_skills.split(',')]
    
    matched_skills = set(user_skills_list).intersection(set(career_skills_list))
    if not career_skills_list:
        return 0
    
    return (len(matched_skills) / len(career_skills_list)) * 100

def parse_json_string(json_string):
    """Parse JSON string safely."""
    if not json_string:
        return {}
    try:
        return json.loads(json_string)
    except:
        return {}

def format_datetime(dt):
    """Format datetime for display."""
    if not dt:
        return ""
    return dt.strftime("%B %d, %Y at %I:%M %p")

def evaluate_code_solution(problem, code, language):
    """Evaluate a coding solution against test cases."""
    test_cases = parse_json_string(problem.test_cases)
    if not test_cases:
        return {"status": "No test cases", "runtime": 0, "memory_used": 0}
    
    # This is a simplified mock evaluator
    # In production, you would use a secure code execution service or sandbox
    
    if language == 'python':
        # Mock evaluation for Python code
        has_syntax_error = False
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError:
            has_syntax_error = True
        
        if has_syntax_error:
            return {"status": "Syntax Error", "runtime": 0, "memory_used": 0}
            
        # For demonstration - check if key functions are defined
        if "two_sum" in problem.title.lower() and "def two_sum" not in code.lower():
            return {"status": "Wrong Answer", "runtime": 100, "memory_used": 5120}
        
        if "reverse" in problem.title.lower() and "def reverse" not in code.lower():
            return {"status": "Wrong Answer", "runtime": 100, "memory_used": 5120}
    
    # Return mock success for demonstration
    return {"status": "Accepted", "runtime": 100, "memory_used": 5120}

def get_coding_problems_sample_data():
    """Return sample coding problems."""
    return [
        {
            "title": "Two Sum",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
            "difficulty": "Easy",
            "topic": "Arrays",
            "example_input": "nums = [2,7,11,15], target = 9",
            "example_output": "[0,1]",
            "test_cases": json.dumps([
                {"input": {"nums": [2,7,11,15], "target": 9}, "output": [0,1]},
                {"input": {"nums": [3,2,4], "target": 6}, "output": [1,2]},
                {"input": {"nums": [3,3], "target": 6}, "output": [0,1]}
            ])
        },
        {
            "title": "Reverse String",
            "description": "Write a function that reverses a string. The input string is given as an array of characters.",
            "difficulty": "Easy",
            "topic": "Strings",
            "example_input": "s = ['h','e','l','l','o']",
            "example_output": "['o','l','l','e','h']",
            "test_cases": json.dumps([
                {"input": {"s": ["h","e","l","l","o"]}, "output": ["o","l","l","e","h"]},
                {"input": {"s": ["H","a","n","n","a","h"]}, "output": ["h","a","n","n","a","H"]}
            ])
        }
    ]

def get_aptitude_test_sample_data():
    """Return sample aptitude test data."""
    return {
        "logical_reasoning": {
            "description": "Test your problem-solving and analytical thinking skills",
            "total_questions": 5,
            "time_limit": None,  # No time limit
            "passing_score": 50,
            "questions": [
                {
                    "question_text": "If all Zips are Zaps, and some Zaps are Zops, then:",
                    "options": [
                        "All Zips are definitely Zops",
                        "Some Zips are definitely Zops",
                        "No Zips are definitely Zops",
                        "None of the above"
                    ],
                    "correct_option": 1,  # 0-indexed
                    "explanation": "Since some Zaps are Zops, and all Zips are Zaps, it's possible that some Zips are Zops, but we can't say for certain that all or none are."
                },
                {
                    "question_text": "Which number should come next in the pattern: 2, 6, 12, 20, 30, ?",
                    "options": ["36", "40", "42", "48"],
                    "correct_option": 2,
                    "explanation": "The pattern follows the difference sequence: +4, +6, +8, +10, +12. So 30 + 12 = 42."
                },
                {
                    "question_text": "If CHAIR = 10 and TABLE = 15, what is STOOL?",
                    "options": ["12", "15", "20", "25"],
                    "correct_option": 0,
                    "explanation": "Each letter value is its position in the alphabet (A=1, B=2, etc.). CHAIR = 3+8+1+9+18 = 39. TABLE = 20+1+2+12+5 = 40. STOOL = 19+20+15+15+12 = 81. Then divide by the number of letters. CHAIR = 39/5 = 7.8 ≈ 8. TABLE = 40/5 = 8. STOOL = 81/5 = 16.2 ≈ 16."
                },
                {
                    "question_text": "A is the father of B. But B is not the son of A. How is that possible?",
                    "options": [
                        "B is A's daughter",
                        "B is A's father",
                        "A is not B's father",
                        "B is adopted"
                    ],
                    "correct_option": 0,
                    "explanation": "B is A's daughter, not son."
                },
                {
                    "question_text": "If you rearrange the letters 'CIFAIPC', you would have the name of a:",
                    "options": [
                        "City", 
                        "Animal", 
                        "Ocean", 
                        "Country"
                    ],
                    "correct_option": 3,
                    "explanation": "CIFAIPC rearranged spells PACIFIC, which is an ocean."
                }
            ]
        },
        "verbal_ability": {
            "description": "Evaluate your language comprehension and communication skills",
            "total_questions": 5,
            "time_limit": None,
            "passing_score": 50,
            "questions": [
                {
                    "question_text": "Choose the word that is most nearly opposite in meaning to 'BENEVOLENT':",
                    "options": ["Charitable", "Malevolent", "Generous", "Kind"],
                    "correct_option": 1,
                    "explanation": "Benevolent means kind and charitable. Malevolent means having or showing a wish to do evil to others."
                },
                {
                    "question_text": "Choose the word that best completes the sentence: The company's profits have _____ over the past five years.",
                    "options": ["Declined", "Stagnated", "Fluctuated", "Stabilized"],
                    "correct_option": 2,
                    "explanation": "Fluctuated means changed irregularly, which makes the most sense in context."
                },
                {
                    "question_text": "Identify the error in the sentence: 'Neither of the candidates have withdrawn from the race.'",
                    "options": [
                        "Neither should be either",
                        "Have should be has",
                        "From should be in",
                        "No error"
                    ],
                    "correct_option": 1,
                    "explanation": "'Neither' is singular, so the verb should be 'has' not 'have'."
                },
                {
                    "question_text": "Choose the pair of words that best expresses a relationship similar to that expressed in the original pair: CANVAS : PAINT",
                    "options": [
                        "Symphony : Orchestra",
                        "Paper : Pencil",
                        "Novel : Writer",
                        "Clay : Sculpture"
                    ],
                    "correct_option": 1,
                    "explanation": "Canvas is the surface on which paint is applied, similarly paper is the surface for pencil."
                },
                {
                    "question_text": "Choose the word that best fits the analogy: Artist is to brush as writer is to:",
                    "options": ["Paper", "Pen", "Novel", "Idea"],
                    "correct_option": 1,
                    "explanation": "An artist uses a brush as a tool, and a writer uses a pen as a tool."
                }
            ]
        }
    }

def get_career_paths_sample_data():
    """Return sample career paths."""
    return [
        {
            "name": "Frontend Developer",
            "description": "Specialize in building user interfaces and web applications that users interact with directly. Work with HTML, CSS, JavaScript and frontend frameworks.",
            "required_skills": "HTML, CSS, JavaScript, React, Angular, Vue.js, UI/UX principles",
            "recommended_courses": "Web Development, User Interface Design, JavaScript Frameworks",
            "job_outlook": "Strong demand with 15% growth projected over the next decade as businesses continue to emphasize web presence and user experience."
        },
        {
            "name": "Backend Developer",
            "description": "Focus on server-side web application logic and integration. Work with databases, server frameworks, APIs, and business logic.",
            "required_skills": "Python, Java, Node.js, SQL, MongoDB, API design, system architecture",
            "recommended_courses": "Database Systems, API Development, Server-side Programming",
            "job_outlook": "Steady growth with 12% increase expected as businesses build more complex applications and services."
        },
        {
            "name": "DevOps Engineer",
            "description": "Bridge the gap between development and operations teams. Automate processes, manage infrastructure, and oversee deployment pipelines.",
            "required_skills": "Linux, Docker, Kubernetes, CI/CD, AWS/Azure/GCP, Infrastructure as Code",
            "recommended_courses": "Cloud Computing, Infrastructure Automation, System Administration",
            "job_outlook": "Rapid growth with 22% increase projected as more organizations adopt DevOps practices for faster, more reliable software delivery."
        },
        {
            "name": "Data Scientist",
            "description": "Extract insights from data using statistical analysis, machine learning, and visualization techniques.",
            "required_skills": "Python, R, SQL, Statistics, Machine Learning, Data Visualization",
            "recommended_courses": "Machine Learning, Statistical Analysis, Big Data Processing",
            "job_outlook": "Very high demand with 31% growth expected as organizations increasingly rely on data-driven decision making."
        },
        {
            "name": "AI Engineer",
            "description": "Design, develop and deploy artificial intelligence models and systems for various applications.",
            "required_skills": "Python, TensorFlow, PyTorch, Deep Learning, Computer Vision, NLP",
            "recommended_courses": "Deep Learning, Natural Language Processing, Reinforcement Learning",
            "job_outlook": "Explosive growth with 40% increase projected as AI continues to transform industries."
        }
    ]

def get_ai_advisor_response(user_message, user_profile=None):
    """Generate a response from the AI Advisor."""
    # In a production environment, this would call the Gemini API
    # This is a simplified mock implementation
    
    user_message_lower = user_message.lower()
    
    # Check for course recommendations
    if "recommend" in user_message_lower and ("course" in user_message_lower or "courses" in user_message_lower):
        return "Based on your profile and interests, I recommend considering these courses: 'Advanced Web Development', 'Data Structures and Algorithms', and 'Machine Learning Fundamentals'. These align well with your career goals and will help build relevant skills."
    
    # Check for career advice
    if "career" in user_message_lower or "job" in user_message_lower:
        return "Looking at the current tech landscape, roles in AI Engineering, Data Science, and Cloud Architecture are showing strong growth. Given your background, focusing on building a portfolio of projects demonstrating your skills would be a great next step. Consider contributing to open-source projects to showcase your abilities to potential employers."
    
    # Check for skill development
    if "skill" in user_message_lower or "learn" in user_message_lower:
        return "For technical skill development, I suggest focusing on: 1) Python programming for data analysis and automation, 2) Cloud services (AWS/Azure/GCP), and 3) Version control with Git. For soft skills, work on communication, problem-solving, and time management through collaborative projects."
    
    # Default response
    return "I'm your AI Career Advisor, here to help with course recommendations, career path exploration, and skill development guidance. Feel free to ask me about career trends, course suggestions, or how to prepare for specific roles in the tech industry."
