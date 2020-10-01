def _100years(name, age, current_year):
    final_year = current_year + (100 - int(age))
    string = "{} will be 100 years old in {}".format(name, final_year)
    return string


if __name__ == "__main__":
    name = input("Name: ")
    age = input("Age: ")
    print(_100years(name, age, 2020))
