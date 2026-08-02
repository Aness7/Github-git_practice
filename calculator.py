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
