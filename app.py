from flask import Flask, render_template, request
import subprocess
import os
import traceback
import ast

app = Flask(__name__)

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
    file_path = os.path.join(TEMP_DIR, "TempCode.java")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        result = subprocess.run(["javac", file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return "No syntax errors detected."
        return result.stderr
    except Exception as e:
        return str(e)

def lint_code_java(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.java")
    with open(file_path, "w") as file:
        file.write(code)

    # Assuming Checkstyle is installed, specify the rules XML file location
    checkstyle_jar = "/path/to/checkstyle.jar"  # Update with your path
    checkstyle_config = "/path/to/checkstyle.xml"  # Update with your path
    try:
        result = subprocess.run(
            ["java", "-jar", checkstyle_jar, "-c", checkstyle_config, file_path],
            capture_output=True, text=True
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def check_runtime_java(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.java")
    class_file = os.path.join(TEMP_DIR, "TempCode")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        # Compile Java code
        compile_result = subprocess.run(["javac", file_path], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return compile_result.stderr

        # Execute Java class
        run_result = subprocess.run(["java", "-cp", TEMP_DIR, "TempCode"], capture_output=True, text=True)
        return run_result.stdout if run_result.returncode == 0 else run_result.stderr
    except Exception as e:
        return str(e)

# Helper functions for C# code analysis
def check_syntax_csharp(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.cs")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        result = subprocess.run(["csc", file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return "No syntax errors detected."
        return result.stderr
    except Exception as e:
        return str(e)

def check_runtime_csharp(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.cs")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        compile_result = subprocess.run(["csc", file_path], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return compile_result.stderr

        run_result = subprocess.run(["mono", os.path.join(TEMP_DIR, "TempCode.exe")], capture_output=True, text=True)
        return run_result.stdout if run_result.returncode == 0 else run_result.stderr
    except Exception as e:
        return str(e)

# Helper functions for C++ code analysis
def check_syntax_cpp(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.cpp")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        result = subprocess.run(["g++", "-fsyntax-only", file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return "No syntax errors detected."
        return result.stderr
    except Exception as e:
        return str(e)

def check_runtime_cpp(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.cpp")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        compile_result = subprocess.run(["g++", file_path, "-o", os.path.join(TEMP_DIR, "TempCode")], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return compile_result.stderr

        run_result = subprocess.run([os.path.join(TEMP_DIR, "TempCode")], capture_output=True, text=True)
        return run_result.stdout if run_result.returncode == 0 else run_result.stderr
    except Exception as e:
        return str(e)

# Helper functions for JavaScript code analysis
def check_syntax_javascript(code):
    # Use Node.js to check for syntax errors
    file_path = os.path.join(TEMP_DIR, "TempCode.js")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        result = subprocess.run(["node", "--check", file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return "No syntax errors detected."
        return result.stderr
    except Exception as e:
        return str(e)

def check_runtime_javascript(code):
    file_path = os.path.join(TEMP_DIR, "TempCode.js")
    with open(file_path, "w") as file:
        file.write(code)

    try:
        run_result = subprocess.run(["node", file_path], capture_output=True, text=True)
        return run_result.stdout if run_result.returncode == 0 else run_result.stderr
    except Exception as e:
        return str(e)

# Flask route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    feedback = {
        "syntax": "",
        "lint": "",
        "runtime": ""
    }
    code = ""
    language = "python"

    if request.method == "POST":
        code = request.form["code"]
        language = request.form["language"]

        if language == "python":
            feedback["syntax"] = check_syntax_python(code)
            feedback["lint"] = lint_code_python(code)
            feedback["runtime"] = check_runtime_python(code)
        elif language == "java":
            feedback["syntax"] = check_syntax_java(code)
            feedback["lint"] = lint_code_java(code)
            feedback["runtime"] = check_runtime_java(code)
        elif language == "csharp":
            feedback["syntax"] = check_syntax_csharp(code)
            feedback["runtime"] = check_runtime_csharp(code)
        elif language == "cpp":
            feedback["syntax"] = check_syntax_cpp(code)
            feedback["runtime"] = check_runtime_cpp(code)
        elif language == "javascript":
            feedback["syntax"] = check_syntax_javascript(code)
            feedback["runtime"] = check_runtime_javascript(code)

    return render_template("indexTesting.html", feedback=feedback, code=code, language=language)

if __name__ == "__main__":
    app.run(debug=True)
