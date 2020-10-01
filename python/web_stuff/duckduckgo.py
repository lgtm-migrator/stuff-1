import urllib.request
import json


def duck_search(search_term):
    search_term = "+".join(search_term.split())
    url = f"https://api.duckduckgo.com/?q={search_term}&format=json"
    content = urllib.request.urlopen(url).read()
    json_content = json.loads(content)
    result = json_content["AbstractText"]
    if json_content["Abstract"] == "":
        result = json_content["RelatedTopics"][0]["Text"]
    return (result)


if __name__ == "__main__":
    print(duck_search(input("Search Term\n> ")))
