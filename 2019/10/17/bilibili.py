"""



pipenv install requests

Origin: https://www.bilibili.com
Range: bytes=920-1203
Referer: https://www.bilibili.com/video/av71189084
Sec-Fetch-Mode: cors
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36


r.text r.content
"""

import requests
import pprint
import re
import json

def header_text_to_dict(header_text):
    return dict(list(map(lambda x: list(map(lambda x: x.strip(), x.split(":", 1))), header_text.split("\n"))))

blbl_header = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,fr;q=0.5
Cache-Control: no-cache
Connection: keep-alive
Host: www.bilibili.com
Pragma: no-cache
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"""

session = requests.Session()

url = "https://www.bilibili.com/video/av71189084"

url = "https://www.bilibili.com/video/av38843284"
res = session.get(url, headers=header_text_to_dict(blbl_header))

# pprint.pprint()
# video_url = re.search(r'"baseUrl":"(.*?),"', res.text).group(1)
video_url = re.search(
    r'<script>window.__playinfo__=(.*?)</script>', res.text).group(1)
title = re.search(
    r'<title.*?>(.*?)</title>', res.text).group(1)
audio_url = json.loads(video_url)['data']['dash']['audio'][0]['baseUrl'].replace('http://', 'https://')

# get video 
# Referer: https://www.bilibili.com/video/av71189084
blbl_video_header = """Origin: https://www.bilibili.com
Sec-Fetch-Mode: cors
User-Agent: Mozilla / 5.0(Macintosh; Intel Mac OS X 10_14_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 77.0 .3865 .120 Safari / 537.36 """

pprint.pprint(audio_url)

download_headers = header_text_to_dict(blbl_video_header)
download_headers['Referer'] = url
download_headers['Range'] = "bytes = 0-907"
res = session.get(audio_url, headers=download_headers)

# pprint.pprint(re.search(r'"baseUrl":"(.*?),"', res.text).group(1))
# pprint.pprint(res.cookies)

pprint.pprint(res.headers['Content-Range'])
pprint.pprint(res.headers['Content-Length'])

audio_length = re.match(
    r'[\s\S]*\/(\d+)', res.headers['Content-Range']).group(1)
pprint.pprint(audio_length)

# download_headers = header_text_to_dict(blbl_video_header)

download_headers['Range'] = f"bytes=0-{audio_length}"
# download_headers['Referer'] = url

download_res = session.get(audio_url, headers=download_headers)
downloaded_file = open(f"{title}.mp4", "wb")
for chunk in download_res.iter_content(chunk_size=256):
    if chunk:
        downloaded_file.write(chunk)


# /usr/local/Cellar/ffmpeg/4.1.4_1/bin/ffmpeg -i 1.mp4 1.mp3
