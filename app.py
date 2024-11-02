from flask import Flask, render_template, request
import ast
import traceback

app = Flask(__name__)


# Helper functions for code analysis
def check_syntax(code):
    try:
        ast.parse(code)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error at line {e.lineno}: {e.msg}"


def lint_code(code):
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


def check_runtime(code):
    try:
        exec(code, {'__builtins__': {'print': print}})
        return "No runtime errors detected."
    except Exception as e:
        return f"Runtime error: {traceback.format_exc()}"


# Flask route for the homepage
@app.route("/", methods=["GET", "POST"])
def indexPython():
    feedback = {
        "syntax": "",
        "lint": "",
        "runtime": ""
    }
    code = ""
    if request.method == "POST":
        code = request.form["code"]
        feedback["syntax"] = check_syntax(code)
        feedback["lint"] = lint_code(code)
        feedback["runtime"] = check_runtime(code)

    return render_template("indexPython.html", feedback=feedback, code=code)


if __name__ == "__main__":
    app.run(debug=True)
