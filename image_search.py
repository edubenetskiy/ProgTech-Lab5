import json

import requests
from bs4 import BeautifulSoup


class Photo:
    id: str
    url: str
    extension: str

    def __init__(self, id, url, extension):
        self.id = id
        self.url = url
        self.extension = extension

    def __str__(self):
        return f"<Photo id={self.id} url={self.url}>"


SEARCH_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

CACHE = {}


def fetch_url_and_parse_html(url, headers):
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, 'html.parser')


def url_for_query(query):
    return f"https://www.google.ru/search?as_st=y&tbm=isch&safe=active&tbs=isz:vga,islt:qsvga,itp:face&as_q={query}"


def search_images(query):
    if query not in CACHE:
        results = []
        url = url_for_query(query)

        while len(results) == 0:
            parsed_html = fetch_url_and_parse_html(url, SEARCH_HEADERS)

            for elem in parsed_html.find_all("div", {"class": "rg_meta"}):
                json_result_text = elem.text
                json_result = json.loads(json_result_text)

                image_id = json_result["id"]
                image_url = json_result["ou"]
                image_format = json_result["ity"]

                photo = Photo(image_id, image_url, image_format)
                results.append(photo)

        CACHE[query] = results

    return CACHE[query]


if __name__ == '__main__':
    images = search_images("Johny Depp")
    print(f"{len(images)} images found:")
    for image in images:
        print(image)
