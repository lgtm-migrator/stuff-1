def even_number(start, end):
    count = 0
    number_list = []
    type = input("From OR Between : ").lower()
    if type == "from":
        end += 1
    elif type == "between":
        end -= 2    for number in range(start, end):
        if number % 2 == 0:
            number_list.append(number)
            count += 1
    output = (f'''
Even Numbers : {count}
List Of Numbers : {number_list}
''')
    return output


if __name__ == "__main__":
    start = int(input("Start: "))
    end = int(input("End: "))
    print(even_number(start, end))
