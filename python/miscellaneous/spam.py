import pyperclip


def spam(word):
    limit = int(input("Character limit\n> "))
    length = limit // len(word)
    output = word * length
    pyperclip.copy(output)
    print("Copied")
    print(len(output))
    return output


if __name__ == "__main__":
    spam(input("Word: "))
