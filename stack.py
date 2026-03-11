class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if not self.is_empty():
            return self.data.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.data[-1]
        return None

    def is_empty(self):
        return len(self.data) == 0

    def __str__(self):
        return str(self.data)


def is_operator(c):
    return c in ['+', '-', '*', '/', '^']


def precedence(op):
    if op == '^':
        return 3
    elif op in ['*', '/']:
        return 2
    elif op in ['+', '-']:
        return 1
    return 0


def is_right_associative(op):
    return op == '^'


def tokenize(expression):
    tokens = []
    num = ""

    for ch in expression.replace(" ", ""):
        if ch.isdigit() or ch == '.':
            num += ch
        else:
            if num:
                tokens.append(num)
                num = ""
            tokens.append(ch)

    if num:
        tokens.append(num)

    return tokens


def infix_to_postfix(tokens):
    stack = Stack()
    output = []
    steps = []

    steps.append("=== PROSES KONVERSI INFIX KE POSTFIX ===")

    for token in tokens:
        if token.replace('.', '', 1).isdigit():  # operand
            output.append(token)
            steps.append(
                f"Token: {token:<5} | Operand -> tambahkan ke output"
                f" | Stack: {stack} | Output: {' '.join(output)}"
            )

        elif token == '(':
            stack.push(token)
            steps.append(
                f"Token: {token:<5} | Push '(' ke stack"
                f" | Stack: {stack} | Output: {' '.join(output)}"
            )

        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                popped = stack.pop()
                output.append(popped)
                steps.append(
                    f"Token: {token:<5} | Pop '{popped}' dari stack ke output"
                    f" | Stack: {stack} | Output: {' '.join(output)}"
                )

            if not stack.is_empty() and stack.peek() == '(':
                stack.pop()
                steps.append(
                    f"Token: {token:<5} | Pop '(' dari stack"
                    f" | Stack: {stack} | Output: {' '.join(output)}"
                )
            else:
                raise ValueError("Kurung tidak seimbang.")

        elif is_operator(token):
            while (
                not stack.is_empty()
                and is_operator(stack.peek())
                and (
                    precedence(stack.peek()) > precedence(token)
                    or (
                        precedence(stack.peek()) == precedence(token)
                        and not is_right_associative(token)
                    )
                )
            ):
                popped = stack.pop()
                output.append(popped)
                steps.append(
                    f"Token: {token:<5} | Pop '{popped}' (prioritas lebih tinggi/sama) ke output"
                    f" | Stack: {stack} | Output: {' '.join(output)}"
                )

            stack.push(token)
            steps.append(
                f"Token: {token:<5} | Push operator '{token}' ke stack"
                f" | Stack: {stack} | Output: {' '.join(output)}"
            )

        else:
            raise ValueError(f"Token tidak valid: {token}")

    while not stack.is_empty():
        if stack.peek() == '(':
            raise ValueError("Kurung tidak seimbang.")
        popped = stack.pop()
        output.append(popped)
        steps.append(
            f"Akhir input | Pop sisa '{popped}' dari stack ke output"
            f" | Stack: {stack} | Output: {' '.join(output)}"
        )

    return output, steps


def apply_operator(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ZeroDivisionError("Pembagian dengan nol tidak diperbolehkan.")
        return a / b
    elif op == '^':
        return a ** b
    else:
        raise ValueError(f"Operator tidak dikenal: {op}")


def evaluate_postfix(postfix_tokens):
    stack = Stack()
    steps = []

    steps.append("\n=== PROSES EVALUASI POSTFIX ===")

    for token in postfix_tokens:
        if token.replace('.', '', 1).isdigit():
            stack.push(float(token))
            steps.append(
                f"Token: {token:<5} | Push operand {token} ke stack"
                f" | Stack: {stack}"
            )

        elif is_operator(token):
            b = stack.pop()
            a = stack.pop()

            if a is None or b is None:
                raise ValueError("Ekspresi tidak valid.")

            result = apply_operator(a, b, token)
            steps.append(
                f"Token: {token:<5} | Pop {a} dan {b}, hitung {a} {token} {b} = {result}"
                f" | Stack sebelum push hasil: {stack}"
            )

            stack.push(result)
            steps.append(
                f"Token: {token:<5} | Push hasil {result} ke stack"
                f" | Stack: {stack}"
            )
        else:
            raise ValueError(f"Token postfix tidak valid: {token}")

    final_result = stack.pop()
    if not stack.is_empty():
        raise ValueError("Ekspresi tidak valid.")

    return final_result, steps


def main():
    print("PROGRAM EVALUASI EKSPRESI ARITMATIKA MENGGUNAKAN STACK")
    infix = input("Masukkan ekspresi infix: ")

    try:
        tokens = tokenize(infix)
        postfix, convert_steps = infix_to_postfix(tokens)
        result, eval_steps = evaluate_postfix(postfix)

        print("\nPostfix Expression:")
        print(" ".join(postfix))

        print("\nStep by Step:")
        for step in convert_steps:
            print(step)
        for step in eval_steps:
            print(step)

        print("\nHasil Akhir:")
        # Tampilkan integer tanpa .0
        if result.is_integer():
            print(int(result))
        else:
            print(result)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    main()