from flask import Flask, render_template, request, redirect
import os
import traceback
import ast
import subprocess
from bs4 import BeautifulSoup
import google.generativeai as genai

app = Flask(__name__)

numbercorrect = 0
ProgrammingLanguage = ""

def log_request():

    InitialPrompt = "Think of a a Question about the "+ProgrammingLanguage +" programming language with A,B, C, and D answer choices. Do not give me the answer"
    genai.configure(api_key='AIzaSyCkZUdo1rRz3o56VPu_p1D0liR-clL_OiQ')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(InitialPrompt)
    global InitialQuestion
    InitialQuestion = response.text.strip()
    return InitialQuestion

def QuestionwithAnswer(userinput):
    global numbercorrect
    FinalPrompt = InitialQuestion + " Respond only with the correct character with no period after it."
    genai.configure(api_key='AIzaSyCkZUdo1rRz3o56VPu_p1D0liR-clL_OiQ')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response2 = model.generate_content(FinalPrompt)
    Answer = response2.text.strip()
    if Answer == userinput.strip():
        numbercorrect += 1

        return "Correct!"   +"\nYou have "+ str(numbercorrect)+" correct"
    else:
        return "False! The correct answer is " + Answer +"\nYou have "+str(numbercorrect)+" correct"

@app.route('/newpage2')
def new_page2():

    generated_string = log_request()
    python_string = generated_string.replace("?","?<br>")
    python_string = python_string.replace("A.","<br>A.")
    python_string = python_string.replace("B.","<br>B.")
    python_string = python_string.replace("C.","<br>C.")
    python_string = python_string.replace("D.","<br>D.")
    return render_template('Question.html', generated_string=generated_string,html_content = python_string)

@app.route('/submit', methods=['POST'])
def submit():
    global numbercorrect
    user_input = request.form['textbox']
    # Save the value as a Python string variable
    Response = QuestionwithAnswer(user_input) #Save the value to be printed into the textbox
    if numbercorrect == 10:
        numbercorrect = 0
        return render_template("10Correct.html")
    else:
        return render_template("Question3.html", InformUser=Response)



@app.route('/new_page')
def new_page():
    return render_template('Question.html')

@app.route('/set_value/<string:value>')
def set_value(value):
    global ProgrammingLanguage
    global Planet
    Planet = value
    if Planet == "Earth":
        ProgrammingLanguage = "Python"
    elif Planet == "Moon":
        ProgrammingLanguage = "Java"
    elif  Planet == "Mars":
        ProgrammingLanguage = "C#"
    elif Planet == "Neptune":
        ProgrammingLanguage = "C++"
    elif Planet == "Saturn":
        ProgrammingLanguage = "JavaScript"
    else:
        ProgrammingLanguage = "HTML"
    return render_template('Prompt.html', value=Planet, ProgrammingLanguage=ProgrammingLanguage)
    



    



TEMP_DIR = "temp_code"
os.makedirs(TEMP_DIR, exist_ok=True)


def check_syntax_html(code):
    try:
        soup = BeautifulSoup(code, 'html.parser')
        # Check for essential tags
        if not soup.head:
            return "Syntax Error: Missing <head> tag."
        if not soup.body:
            return "Syntax Error: Missing <body> tag."
        # Check for meta tag
        if '<meta charset=' in code and '>' not in code.split('<meta charset=')[1]:
            return "Syntax Error: Missing closing '>' in <meta> tag."
        if '<title>' in code and '</title>' not in code:
            return "Syntax Error: Missing closing </title> tag."
        return "No syntax errors detected."
    except Exception as e:
        return f"Syntax Error: {str(e)}"


def lint_code_html(code):
    suggestions = []
    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > 120:
            suggestions.append(f"Line {i}: Exceeds 120 characters.")
        if "<script" in line and not line.strip().endswith("</script>"):
            suggestions.append(f"Line {i}: Missing closing </script> tag.")
        if "<h1>" in line and not "</h1>" in line:
            suggestions.append(f"Line {i}: Missing closing </h1> tag.")

    return "\n".join(suggestions) if suggestions else "No linting issues detected."


# Python code analysis
def check_syntax_python(code):
    try:
        ast.parse(code)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error at line {e.lineno}: {e.msg}"


def lint_code_python(code):
    suggestions = []
    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > 79:
            suggestions.append(f"Line {i}: Exceeds 79 characters.")
        if "==" in line and " if " not in line:
            suggestions.append(f"Line {i}: Consider using 'is' for equality checks on singletons (e.g., None).")
        if line.strip().startswith("print"):
            suggestions.append(f"Line {i}: Avoid print statements in production code.")

    return "\n".join(suggestions) if suggestions else "No linting issues detected."


def check_runtime_python(code):
    try:
        exec(code, {'__builtins__': {'print': print}})
        return "No runtime errors detected."
    except Exception as e:
        return f"Runtime error: {traceback.format_exc()}"


# Java code analysis
def check_syntax_java(code):
    try:
        with open("temp_code/Test.java", "w") as f:
            f.write(code)
        subprocess.run(["javac", "temp_code/Test.java"], check=True)
        return "No syntax errors detected."
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else "Compilation failed without error message."
        return f"Syntax Error: {error_message}"


def lint_code_java(code):
    suggestions = []
    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > 120:
            suggestions.append(f"Line {i}: Exceeds 120 characters.")
        if "System.out.println" in line:
            if "divide(" in line and "0" in line:
                suggestions.append(f"Line {i}: Potential division by zero in divide() call.")
        if "if (" in line and "==" in line and "0" in line:
            suggestions.append(f"Line {i}: Consider checking for division by zero before calling divide().")

    return "\n".join(suggestions) if suggestions else "No linting issues detected."


def check_runtime_java(code):
    try:
        with open("temp_code/Test.java", "w") as f:
            f.write(code)
        subprocess.run(["javac", "temp_code/Test.java"], check=True)
        result = subprocess.run(["java", "-cp", "temp_code", "Test"], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"Runtime error: {result.stderr}"
    except Exception as e:
        return f"Runtime error: {traceback.format_exc()}"


# JavaScript code analysis
def check_syntax_javascript(code):
    try:
        with open("temp_code/test.js", "w") as f:
            f.write(code)
        subprocess.run(["node", "-c", "temp_code/test.js"], check=True)
        return "No syntax errors detected."
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else "Compilation failed without error message."
        return f"Syntax Error: {error_message}"


def lint_code_javascript(code):
    suggestions = []
    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        if line.strip().endswith(';') and not line.strip().startswith('//'):
            suggestions.append(f"Line {i}: Missing semicolon at the end of the statement.")
        if len(line) > 80:
            suggestions.append(f"Line {i}: Exceeds 80 characters.")

    return "\n".join(suggestions) if suggestions else "No linting issues detected."


def check_runtime_javascript(code):
    try:
        with open("temp_code/test.js", "w") as f:
            f.write(code)
        result = subprocess.run(["node", "temp_code/test.js"], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"Runtime error: {result.stderr}"
    except Exception as e:
        return f"Runtime error: {traceback.format_exc()}"


# Route to handle the root URL and redirect to Python by default
@app.route("/", methods=["GET"])
def home():
    return redirect("/python")


# Route to handle different languages
@app.route("/<language>", methods=["GET", "POST"])
def index(language="python"):
    feedback = {"syntax": "", "lint": "", "runtime": ""}
    code = ""

    if request.method == "POST":
        code = request.form["code"]
        if code.strip():  # Check if there is any code input
            if language == "python":
                feedback["syntax"] = check_syntax_python(code)
                feedback["lint"] = lint_code_python(code)
                feedback["runtime"] = check_runtime_python(code)
            elif language == "java":
                feedback["syntax"] = check_syntax_java(code)
                feedback["lint"] = lint_code_java(code)
                feedback["runtime"] = check_runtime_java(code)
            elif language == "html":
                feedback["syntax"] = check_syntax_html(code)
                feedback["lint"] = lint_code_html(code)
                feedback["runtime"] = "HTML does not support runtime checks."
            elif language == "javascript":
                feedback["syntax"] = check_syntax_javascript(code)
                feedback["lint"] = lint_code_javascript(code)
                feedback["runtime"] = check_runtime_javascript(code)

    return render_template("index.html", feedback=feedback, code=code, language=language)
    


if __name__ == "__main__":
    app.run(debug=True)
