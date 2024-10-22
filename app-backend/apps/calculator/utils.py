import google.generativeai as ai
import ast
import json
from PIL import Image
from constants import GEMINI_API_KEY


ai.configure(api_key=GEMINI_API_KEY)

model = ai.GenerativeModel(model_name="gemini-1.5-flash")

def process_image(img: Image, dict_of_vars:dict):
    dict_of_vars_to_str = json.dumps(dict_of_vars, ensure_ascii=False)
    # prompt = (
    # "You are given an image containing mathematical expressions, equations, or graphical problems. "
    # "Solve them following the PEMDAS rule: Parentheses, Exponents, Multiplication/Division (left to right), "
    # "and Addition/Subtraction (left to right). "
    # "Example: "
    # "Q1. 2 + 3 * 4 => (3 * 4) = 12; 2 + 12 = 14. "
    # "Q2. 2 + 3 + 5 * 4 - 8 / 2 => (5 * 4) = 20; (8 / 2) = 4; (2 + 3) = 5; 5 + 20 = 25; 25 - 4 = 21. "
    # "There are five types of problems in the image. Only one case will apply each time: "
    
    # "1. **Simple Mathematical Expressions:** Solve expressions like 2 + 2, 3 * 4, etc. "
    # "Return a LIST with one DICT: [{'expr': 'given expression', 'result': calculated_answer}]. "
    
    # "2. **Set of Equations:** Solve for variables in equations like x^2 + 2x + 1 = 0, 3y + 4x = 0, etc. "
    # "Return a COMMA SEPARATED LIST of DICTS, one for each variable: [{'expr': 'x', 'result': value, 'assign': True}]. "
    
    # "3. **Variable Assignments:** Handle assignments like x = 4, y = 5, etc. "
    # "Return a LIST of DICTS: [{'expr': 'x', 'result': 4, 'assign': True}]. "
    
    # "4. **Graphical Math Problems:** Solve word problems based on drawings, such as trigonometry, collisions, etc. "
    # "Return a LIST with one DICT: [{'expr': 'given problem', 'result': calculated answer}]. "
    
    # "5. **Abstract Concept Detection:** Identify abstract ideas from drawings (e.g., love, patriotism). "
    # "Return a LIST with one DICT: [{'expr': 'explanation', 'result': 'abstract concept'}]. "
    
    # "Use the following dictionary of user-assigned variables if any appear in the expression: {dict_of_vars_str}. "
    # "Escape characters like \\f and \\n should be written as \\\\f and \\\\n. "
    # "DO NOT USE backticks or Markdown formatting. "
    # "Ensure all dictionary keys and values are properly quoted for easy parsing with Python's ast.literal_eval."
    # )

    prompt = (
    "You are given an image containing mathematical expressions, equations, or graphical problems. "
    "Solve them following the PEMDAS rule: Parentheses, Exponents, Multiplication/Division (left to right), "
    "and Addition/Subtraction (left to right). "
    "After solving, explain the steps taken to reach the solution in detail. "
    "The output must contain the final result as well as a step-by-step breakdown of how the solution was reached."
    
    "Example: "
    "Q1. 2 + 3 * 4 => (3 * 4) = 12; 2 + 12 = 14. "
    "Explanation: "
    "1. First, multiply 3 by 4 to get 12. "
    "2. Then, add 2 to 12 to get 14. "
    "Final result: 14."
    
    "Q2. 2 + 3 + 5 * 4 - 8 / 2 => (5 * 4) = 20; (8 / 2) = 4; (2 + 3) = 5; 5 + 20 = 25; 25 - 4 = 21. "
    "Explanation: "
    "1. First, multiply 5 by 4 to get 20. "
    "2. Then, divide 8 by 2 to get 4. "
    "3. Add 2 and 3 to get 5. "
    "4. Now, add 5 and 20 to get 25. "
    "5. Finally, subtract 4 from 25 to get 21. "
    "Final result: 21."
    
    "There are five types of problems in the image. Only one case will apply each time: "
    
    "1. **Simple Mathematical Expressions:** Solve expressions like 2 + 2, 3 * 4, etc. "
    "Return a LIST with one DICT: [{'expr': 'given expression', 'result': calculated_answer, 'steps': ['step1', 'step2', '...'], 'explanation': 'step-by-step explanation'}]. "
    
    "2. **Set of Equations:** Solve for variables in equations like x^2 + 2x + 1 = 0, 3y + 4x = 0, etc. "
    "Return a COMMA SEPARATED LIST of DICTS, one for each variable: [{'expr': 'x', 'result': value, 'assign': True, 'steps': ['step1', 'step2', '...'], 'explanation': 'steps used to solve'}]. "
    
    "3. **Variable Assignments:** Handle assignments like x = 4, y = 5, etc. "
    "Return a LIST of DICTS: [{'expr': 'x', 'result': 4, 'assign': True, 'steps': ['variable assignment explanation'], 'explanation': 'variable was assigned to value 4'}]. "
    
    "4. **Graphical Math Problems:** Solve word problems based on drawings, such as trigonometry, collisions, etc. "
    "Return a LIST with one DICT: [{'expr': 'given problem', 'result': calculated answer, 'steps': ['step1', 'step2', '...'], 'explanation': 'steps used to solve'}]. "
    
    "5. **Abstract Concept Detection:** Identify abstract ideas from drawings (e.g., love, patriotism). "
    "Return a LIST with one DICT: [{'expr': 'explanation', 'result': 'abstract concept', 'steps': ['abstract detection steps'], 'explanation': 'reason behind detection of abstract concept'}]. "
    
    "Use the following dictionary of user-assigned variables if any appear in the expression: {dict_of_vars_str}. "
    "Escape characters like \\f and \\n should be written as \\\\f and \\\\n. "
    "DO NOT USE backticks or Markdown formatting. "
    "Ensure all dictionary keys and values are properly quoted for easy parsing with Python's ast.literal_eval."
)



    response = model.generate_content([prompt, img])

    print(response.text)

    answers = []

    try:
        answers = ast.literal_eval(response.text)
    except Exception as error:
        print(f"Sorry andi..!, ERROR {error}")

    print("answers: ", answers)
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
    return answers



