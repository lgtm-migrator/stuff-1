def fizzbuzz(input):
    if (input % 3 == 0) and (input % 5 == 0):
        return 'Fizz Buzz'
    elif input % 3 == 0:
        return 'Fizz'
    elif input % 5 == 0:
        return 'Buzz'
    return input


while __name__ == "__main__":
    print(fizzbuzz(int(input("Number : "))))
