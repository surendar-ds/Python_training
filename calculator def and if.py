print("      ======Caculator======")
print("          Addition(+)")
print("          Subraction(-)")
print("          Multiplication(*)")
print("          Division(/)")
print("          Modulus(%)")
def cal(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return "Division by 0 error"
        else:
            return a / b
    elif op == '%':
        return a % b
    else:
        return "Invalid operation"

while True:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    choice = input("Enter operation (+, -, *, /, %) or 'exit' to quit: ")
    if choice == 'exit':
        print("Calculator closed.")
        break
    result = cal(num1, num2, choice)
    print("Result =", result)
    print()