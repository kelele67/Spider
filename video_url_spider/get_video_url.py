import re
import csv
import requests
from bs4 import BeautifulSoup


def write_csv(filename, datas):
    with open('%s_list.csv' % filename, 'a', encoding='utf8') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(datas)


def get_url_list():
    filename = "url"
    for i in range(1, 10):
        # base_url = "https://av28.com/videos/wife\?o\=mv&page=" + str(i)
        base_url = "https://av28.com/search/videos?search_query=NTR&page=" + str(i)
        print (base_url)
        response = requests.get(base_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html5lib")
        url_list = soup.find('div', 'col-md-9 col-sm-8')
        urls = url_list.find_all('div', 'well well-sm')
        for url_info in urls:
            url_match = re.search('href=".*?"', str(url_info))
            try:
                url = "https://av28.com" + url_match.group(0)[6:-1]
            except:
                url = ""
            print (url)
            datas = [url]
            write_csv(filename, datas)
            if url:
                get_video_url(url)
        print ("--------")  


def get_video_url(url):
    filename = "video"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html5lib")
    video_url_info = soup.find('div', 'video-container')
    # print (video_url_info)
    video_url_match = re.search('src=".*?"', str(video_url_info))
    try:
        video_url = video_url_match.group(0)[5:-1]
        video_url = video_url.replace(';', '&')
    except:
        video_url = ""
    print (video_url)
    datas = [video_url]
    write_csv(filename, datas)


if __name__ == '__main__':
    # base_url = "https://av28.com/videos/wife\?o\=mv?page="
    get_url_list()
