# encoding=utf-8
import requests
import re
import json


def get_one_page(url):
    headers = {
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 53.0.2785.104Safari / 537.36Core / 1.53.4882.400QQBrowser / 9.7.13059.400'
    }
    response = requests.get(url, headers=headers)
    if 200 == response.status_code:
        return response.text.encode(response.encoding).decode(response.apparent_encoding)
    return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index-\d*">(\d*)</i>.*?data-src="(.*?)".*?name"><a'
                         '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].replace('\n', '').strip()[3:],
            'time': item[4][5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    f = open('../data/maoyan_result.txt', 'a+', encoding='utf-8')
    f.writelines(json.dumps(content, ensure_ascii=False) + '\n')
    f.close()


if __name__ == '__main__':
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset=' + str(i * 10)
        html = get_one_page(url)
        for item in parse_one_page(html):
            write_to_file(item)