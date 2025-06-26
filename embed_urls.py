import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

def find_embed_urls(video_url):
    try:
        res = requests.get(video_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Error fetching {video_url}: {e}")
        return []

    soup = BeautifulSoup(res.text, 'html.parser')

    embed_urls = []
    iframes = soup.find_all('iframe')
    for iframe in iframes:
        src = iframe.get('src')
        if src:
            # 相対パスの場合は絶対URLに補完
            if src.startswith('/'):
                src = 'https://www.tokyomotion.net' + src
            embed_urls.append(src)

    if not embed_urls:
        print(f"No embed iframe found in {video_url}")

    return embed_urls

if __name__ == "__main__":
    embed_urls = []
    with open('video_urls.txt', 'r', encoding='utf-8') as f:
        video_urls = [line.strip() for line in f if line.strip()]

    for url in video_urls:
        print(f"Checking {url} ...")
        found_urls = find_embed_urls(url)
        embed_urls.extend(found_urls)
        time.sleep(1)  # サイト負荷軽減のため少し待つ

    # 重複を除去
    embed_urls = list(set(embed_urls))

    with open('embed_urls.txt', 'w', encoding='utf-8') as f:
        for eurl in embed_urls:
            f.write(eurl + '\n')

    print(f"Found {len(embed_urls)} embed URLs. Saved to embed_urls.txt")
