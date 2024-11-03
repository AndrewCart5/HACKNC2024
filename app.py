from flask import Flask, render_template, request, redirect
import os
import traceback
import ast
import subprocess
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML linting

app = Flask(__name__, template_folder='.')  # Set template folder to current directory

# Directory for temporary files
TEMP_DIR = "temp_code"
os.makedirs(TEMP_DIR, exist_ok=True)


# Helper functions for Python code analysis
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


# Helper functions for Java code analysis
def check_syntax_java(code):
    try:
        with open("temp_code/Test.java", "w") as f:
            f.write(code)
        subprocess.run(["javac", "temp_code/Test.java"], check=True)
        return "No syntax errors detected."
    except subprocess.CalledProcessError as e:
        return f"Syntax Error: {e.stderr.decode()}"


def lint_code_java(code):
    suggestions = []
    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > 120:
            suggestions.append(f"Line {i}: Exceeds 120 characters.")
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


# Helper functions for HTML code analysis
def check_syntax_html(code):
    try:
        soup = BeautifulSoup(code, "html.parser")
        return "No syntax errors detected in HTML." if soup else "HTML code may have syntax issues."
    except Exception as e:
        return f"HTML syntax error: {str(e)}"


def lint_code_html(code):
    suggestions = []
    soup = BeautifulSoup(code, "html.parser")

    # Check for missing <title> tag
    if not soup.title:
        suggestions.append("HTML is missing a <title> tag.")

    # Check for header tags
    if not any(soup.find(tag) for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]):
        suggestions.append("HTML is missing header tags (e.g., <h1>, <h2>).")

    # Check for viewport meta tag
    if not soup.find("meta", {"name": "viewport"}):
        suggestions.append("HTML is missing a viewport meta tag for responsive design.")

    # Check for missing alt attribute in <img> tags
    for img in soup.find_all("img"):
        if not img.get("alt"):
            suggestions.append("Image tag is missing an 'alt' attribute.")

    # Check for overly long lines
    lines = code.splitlines()
    for i, line in enumerate(lines, start=1):
        if len(line) > 120:
            suggestions.append(f"Line {i}: Exceeds 120 characters.")

    return "\n".join(suggestions) if suggestions else "No linting issues detected in HTML."


# Route to handle the root URL and redirect to Python by default
@app.route("/", methods=["GET"])
def home():
    return redirect("/python")  # Redirect to the default language (Python)


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

    return render_template("index.html", feedback=feedback, code=code, language=language)


if __name__ == "__main__":
    app.run(debug=True)
