print("Welcome to the calculator program")

#Calculator program for chosen operation
a= float(input("Enter first number: "))
operation = input("Choose operation: +, -, x, / : ")
b= float(input("Enter second number: "))

if operation == "+":
    result = a + b

elif operation == "-":
    result = a - b

elif operation == "x":
    result = a * b

elif operation == "/":
    if b == 0:
        print("Error: Division by zero is not allowed.")
    else:
        result = a / b
print("The result is: ", result)

"""
#Calcuator that gives the result of main 4 operations from two numbers
#Addition operation
a= int(input("Enter first number: "))
b= int(input("Enter second number: "))
add= a + b    
print("The sum is: ", add)

#Subtraction operation
sub= a - b
print("The difference is: ", sub)

#Multiplication operation
mul= a * b
print("The product is: ", mul)

#Division operation
if b == 0:
    print("Error: Division by zero is not allowed.")
else:
    div= a / b
    print("The quotient is: ", div)

"""

#AI generated code 
"""
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero."
    return a / b

def main():
    print("Calculator")

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    print("Addition =", add(num1, num2))
    print("Subtraction =", subtract(num1, num2))
    print("Multiplication =", multiply(num1, num2))
    print("Division =", divide(num1, num2))

if __name__ == "__main__":
    main()
"""
