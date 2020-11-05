def emote_convert(words, message=False):
    convert = {
        "a": "🇦",
        "b": "🇧",
        "c": "🇨",
        "d": "🇩",
        "e": "🇪",
        "f": "🇫",
        "g": "🇬",
        "h": "🇭",
        "i": "🇮",
        "j": "🇯",
        "k": "🇰",
        "l": "🇱",
        "m": "🇲",
        "n": "🇳",
        "o": "🇴",
        "p": "🇵",
        "q": "🇶",
        "r": "🇷",
        "s": "🇸",
        "t": "🇹",
        "u": "🇺",
        "v": "🇻",
        "w": "🇼",
        "x": "🇽",
        "y": "🇾",
        "z": "🇿"
    }
    words = words.lower()
    if message:
        output = ""
        for word in words:
            output += convert.get(word, word) + " "
        return output
    emote_list = []
    for word in words:
        emote_list.append((word, convert.get(word, word)))
    return emote_list


def fallback_emote(emote_list):
    fallback = {
        "a": "🅰️",
        "b": "🅱️",
        "m": "Ⓜ️",
        "o": "🅾️"
    }
    character = emote_list[0][0]
    output = (character, fallback.get(character, character))
    if character not in list(fallback.keys()):
        output = emote_list
    return output
