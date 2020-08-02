import urllib.request
import json


def download(url):
    content = urllib.request.urlopen(url).read()
    content = json.loads(content)
    return content


def convert(data, currency, value):
    currency = currency.upper()
    base_currency = data["base"]
    conversion_rate = data["rates"][currency]
    converted_amount = float(value) * conversion_rate
    result = "{} {} converted from {} at the conversion rate of {}".format(
        converted_amount, currency, base_currency, conversion_rate)
    print(result)


def main():
    api_key = "API"
    url = "http://data.fixer.io/api/latest?access_key={}&format=1".format(
        api_key)
    content = download(url)
    print("Converting from {}".format(content["base"]))
    convert(content, input("Currency : "), input("Value : "))


if __name__ == "__main__":
    main()
