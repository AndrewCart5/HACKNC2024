// JavaScript Test
function testFunction() {
    console.log("This is a valid line."); // This is fine

    // Syntax Error: Missing closing parenthesis
    console.log("This line has a missing parenthesis"; 

    // Linting Issue: Missing semicolon
    let a = 5
    let b = 10;

    // Logic Error: This will cause a runtime error when dividing by zero
    let result = divide(a, 0); // This will throw an error

    // Unused variable
    let unusedVariable = "I am not used anywhere";

    // Warning: Too many arguments
    console.log("Too many arguments", a, b, result, "Extra argument");

    // Missing return statement (no return in a function with a return type)
    return
}

// Function that causes a runtime error
function divide(x, y) {
    if (y === 0) {
        throw new Error("Cannot divide by zero!"); // Custom error for clarity
    }
    return x / y;
}

// Call the test function
testFunction();
