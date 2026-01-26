import sys
import platform

def is_palindrome(number):
    original = number
    reverse = 0

    while number > 0:
        digit = number % 10
        reverse = reverse * 10 + digit
        number //= 10

    return original == reverse


if __name__ == "__main__":
    print("Hello, Algorithms!")
    print(f"Python Version: {sys.version}")
    print(f"Operating System: {platform.system()} {platform.release()}")

    num = 121
    result = is_palindrome(num)

    if result:
        print(f"The number {num} is a palindrome.")
    else:
        print(f"The number {num} is not a palindrome.")
