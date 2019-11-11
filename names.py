from bs4 import BeautifulSoup

import requests

NAMES = None


def get_famous_names():
    global NAMES
    if NAMES is None:
        response = requests.get("https://www.biographyonline.net/people/famous-100.html").text
        soup = BeautifulSoup(response, 'html.parser')
        lis = soup.find("ol").find_all("li")
        NAMES = [el.find("a").text.strip() for el in lis if el.find("a")]
    return list(NAMES)


if __name__ == '__main__':
    names = get_famous_names()
    print(names)
