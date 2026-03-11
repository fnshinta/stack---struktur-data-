import java.util.Scanner;

public class stack2 {

    static class CharStack {
        char[] data;
        int top;

        CharStack(int size) {
            data = new char[size];
            top = -1;
        }

        void push(char c) {
            data[++top] = c;
        }

        char pop() {
            return data[top--];
        }

        char peek() {
            return data[top];
        }

        boolean isEmpty() {
            return top == -1;
        }

        String display() {
            String hasil = "[";
            for (int i = 0; i <= top; i++) {
                hasil += data[i];
                if (i < top) hasil += ", ";
            }
            hasil += "]";
            return hasil;
        }
    }

    static class DoubleStack {
        double[] data;
        int top;

        DoubleStack(int size) {
            data = new double[size];
            top = -1;
        }

        void push(double x) {
            data[++top] = x;
        }

        double pop() {
            return data[top--];
        }

        boolean isEmpty() {
            return top == -1;
        }

        String display() {
            String hasil = "[";
            for (int i = 0; i <= top; i++) {
                hasil += data[i];
                if (i < top) hasil += ", ";
            }
            hasil += "]";
            return hasil;
        }
    }

    static boolean isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '^';
    }

    static int precedence(char op) {
        if (op == '^') return 3;
        if (op == '*' || op == '/') return 2;
        if (op == '+' || op == '-') return 1;
        return 0;
    }

    static boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }

    static String infixToPostfix(String infix) {
        CharStack stack = new CharStack(infix.length());
        String postfix = "";

        System.out.println("=== PROSES KONVERSI INFIX KE POSTFIX ===");

        for (int i = 0; i < infix.length(); i++) {
            char ch = infix.charAt(i);

            if (ch == ' ') {
                continue;
            }

            if (isDigit(ch)) {
                while (i < infix.length() && (isDigit(infix.charAt(i)) || infix.charAt(i) == '.')) {
                    postfix += infix.charAt(i);
                    i++;
                }
                postfix += " ";
                i--;

                System.out.println("Baca operand -> output: " + postfix + " | Stack: " + stack.display());
            } else if (ch == '(') {
                stack.push(ch);
                System.out.println("Push '(' -> Stack: " + stack.display());
            } else if (ch == ')') {
                while (!stack.isEmpty() && stack.peek() != '(') {
                    char op = stack.pop();
                    postfix += op + " ";
                    System.out.println("Pop '" + op + "' ke output -> " + postfix + " | Stack: " + stack.display());
                }
                if (!stack.isEmpty() && stack.peek() == '(') {
                    stack.pop();
                    System.out.println("Pop '(' -> Stack: " + stack.display());
                }
            } else if (isOperator(ch)) {
                while (!stack.isEmpty() && isOperator(stack.peek()) &&
                       precedence(stack.peek()) >= precedence(ch)) {
                    char op = stack.pop();
                    postfix += op + " ";
                    System.out.println("Pop '" + op + "' karena prioritas -> output: " + postfix + " | Stack: " + stack.display());
                }
                stack.push(ch);
                System.out.println("Push operator '" + ch + "' -> Stack: " + stack.display());
            }
        }

        while (!stack.isEmpty()) {
            char op = stack.pop();
            postfix += op + " ";
            System.out.println("Pop sisa '" + op + "' -> output: " + postfix + " | Stack: " + stack.display());
        }

        return postfix;
    }

    static double applyOperator(double a, double b, char op) {
        if (op == '+') return a + b;
        if (op == '-') return a - b;
        if (op == '*') return a * b;
        if (op == '/') return a / b;
        if (op == '^') return Math.pow(a, b);
        return 0;
    }

    static double evaluatePostfix(String postfix) {
        DoubleStack stack = new DoubleStack(postfix.length());

        System.out.println("\n=== PROSES EVALUASI POSTFIX ===");

        int i = 0;
        while (i < postfix.length()) {
            char ch = postfix.charAt(i);

            if (ch == ' ') {
                i++;
                continue;
            }

            if (isDigit(ch)) {
                String numStr = "";
                while (i < postfix.length() &&
                      (isDigit(postfix.charAt(i)) || postfix.charAt(i) == '.')) {
                    numStr += postfix.charAt(i);
                    i++;
                }

                double num = Double.parseDouble(numStr);
                stack.push(num);
                System.out.println("Push " + num + " -> Stack: " + stack.display());
            } else if (isOperator(ch)) {
                if (!stack.isEmpty()) {
                    double b = stack.pop();
                    double a = stack.pop();
                    double hasil = applyOperator(a, b, ch);

                    System.out.println("Pop " + a + " dan " + b + ", hitung " + a + " " + ch + " " + b + " = " + hasil);

                    stack.push(hasil);
                    System.out.println("Push hasil " + hasil + " -> Stack: " + stack.display());
                }
                i++;
            } else {
                i++;
            }
        }

        return stack.pop();
    }

    public static void main(String[] args) {
        try (Scanner input = new Scanner(System.in)) {
            System.out.print("Masukkan ekspresi infix: ");
            String infix = input.nextLine();

            String postfix = infixToPostfix(infix);

            System.out.println("\nPostfix Expression:");
            System.out.println(postfix);

            double hasil = evaluatePostfix(postfix);

            System.out.println("\nHasil Akhir:");
            if (hasil == (int) hasil) {
                System.out.println((int) hasil);
            } else {
                System.out.println(hasil);
            }
        }
    }
}