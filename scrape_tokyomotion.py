import requests
from bs4 import BeautifulSoup
import re
import time

def get_video_urls(channel_url):
    video_urls = []
    page_url = channel_url

    while True:
        print(f"Fetching: {page_url}")
        res = requests.get(page_url)
        if res.status_code != 200:
            print("Failed to retrieve page.")
            break

        soup = BeautifulSoup(res.text, 'html.parser')

        links = soup.find_all('a', href=True)
        for a in links:
            href = a['href']
            if re.match(r'^/video/\d+', href):
                full_url = 'https://www.tokyomotion.net' + href
                if full_url not in video_urls:
                    video_urls.append(full_url)

        next_page = soup.find('a', string=re.compile(r'次へ|Next'))
        if next_page and 'href' in next_page.attrs:
            page_url = 'https://www.tokyomotion.net' + next_page['href']
            time.sleep(1)
        else:
            break

    return video_urls

if __name__ == "__main__":
    channel_url = 'https://www.tokyomotion.net/user/nirvanakamo/videos'
    urls = get_video_urls(channel_url)
    print(f"\nFound {len(urls)} videos:")
    for url in urls:
        print(url)

    with open('video_urls.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')
    print("動画URLをvideo_urls.txtに保存しました。")
