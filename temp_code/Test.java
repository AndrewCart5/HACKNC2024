// Java Test Case
public class Test {
    public static void main(String[] args) {
        System.out.println(add(2, 3)); // Missing return type in add method
        System.out.println(divide(10, 0)); // Division by zero
    }
    
    // Incorrectly defined add method, missing return type
    public static add(int a, int b) { // Missing return type
        return a + b;
    }

    // Method to divide two numbers
    public static int divide(int a, int b) {
        return a / b; // Division by zero if b is 0
    }
}

