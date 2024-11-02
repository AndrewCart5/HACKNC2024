import ast
import traceback


# Main function to handle user input and provide feedback
def rubber_duck():
    print("Welcome to Rubber Duck AI! Enter your code below, and I'll help you debug.")
    while True:
        print("\nType 'exit' to quit.")
        user_code = input("\nPlease enter your code snippet:\n")

        if user_code.strip().lower() == "exit":
            print("Goodbye!")
            break

        # Provide feedback
        syntax_feedback = check_syntax(user_code)
        lint_feedback = lint_code(user_code)
        runtime_feedback = check_runtime(user_code)

        print("\n--- Feedback ---")
        print("Syntax Check:")
        print(syntax_feedback)

        print("\nLint Check:")
        print(lint_feedback)

        print("\nRuntime Feedback:")
        print(runtime_feedback)


# Function to check for syntax errors
def check_syntax(code):
    try:
        ast.parse(code)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error at line {e.lineno}: {e.msg}"


# Function to provide basic linting (catching potential issues or style suggestions)
def lint_code(code):
    suggestions = []
    lines = code.splitlines()

    # Check for common linting issues
    for i, line in enumerate(lines, start=1):
        if len(line) > 79:
            suggestions.append(f"Line {i}: Exceeds 79 characters.")
        if "==" in line and " if " not in line:
            suggestions.append(f"Line {i}: Consider using 'is' for equality checks on singletons (e.g., None).")
        if line.strip().startswith("print"):
            suggestions.append(f"Line {i}: Avoid print statements in production code.")

    return "\n".join(suggestions) if suggestions else "No linting issues detected."


# Function to check runtime errors by running the code in a safe environment
def check_runtime(code):
    try:
        # Allow only safe built-ins, like print
        exec(code, {'__builtins__': {'print': print}})
        return "No runtime errors detected."
    except Exception as e:
        return f"Runtime error: {traceback.format_exc()}"

# Run the rubber duck assistant
if __name__ == "__main__":
    rubber_duck()
