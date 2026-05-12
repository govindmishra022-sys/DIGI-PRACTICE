def add_numbers(num1, num2):
    return num1 + num2

if __name__ == "__main__":
    try:
        n1 = float(input("Enter the first number: "))
        n2 = float(input("Enter the second number: "))
        result = add_numbers(n1, n2)
        print(f"The sum of {n1} and {n2} is {result}")
    except ValueError:
        print("Invalid input. Please enter numbers only.")
