import pyperclip
import argparse


def string_split(string):
    print("Current string is {} characters long".format(len(string)))
    max_len = int(input("Max length: "))
    if len(string) <= max_len:
        print("There is nothing to do")
        return
    new_str = ""
    while string != "":
        new_str += string[:max_len] + "/|"
        string = string[max_len:]
    str_list = new_str.split("/|")
    str_list.pop(-1)
    count = 0
    str_count = len(str_list)
    for string in str_list:
        count += 1
        input_ = input("Press ENTER to copy string {} of {}".format(
            count, str_count))
        if '' in input_:
            pyperclip.copy(string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        help="Read contents from a specific file")
    args = parser.parse_args()
    if args.file is not None:
        with open(args.file, "r") as f:
            string = f.read()
    else:
        string = input("String: ")
    string_split(string)
