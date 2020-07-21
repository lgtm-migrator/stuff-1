def emoji_converter(message):
    words = message.split(' ')
    emoji_mapping = {
        ":)":  "😃",
        ":(": "😟",
        ":*": "😘",
        ":'(": "😢",
        ":/": "😕",
        "/shrug": r"¯\_(ツ)_/¯"
    }
    output = ''
    for word in words:
        output += emoji_mapping.get(word, word) + ' '
    return output


if __name__ == "__main__":
    output = emoji_converter(input("> "))
    print(output)
