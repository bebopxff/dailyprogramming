"""

https://raw.githubusercontent.com/jnoodle/common-programming-words-english-pronunciation/master/README.md

| access | [<img src="audio1.png" width="24">](http://dict.youdao.com/dictvoice?audio=access&type=2)&nbsp;&nbsp;[<img src="audio2.png" width="24">](https://audio00.forvo.com/audios/mp3/1/p/1p_8975595_39_283368_36283.mp3) | 存取，访问 | `/'æksɛs/` 注意重音 |

https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence

https://stackoverflow.com/questions/10569438/how-to-print-unicode-character-in-python

https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests

https://stackoverflow.com/questions/45954949/parse-text-response-from-http-request-in-python

https://www.rexegg.com/regex-quickstart.html need proxy 
"""

import requests
import pprint
import uuid
import json
import re 

test_line = """| access | [<img src="audio1.png" width="24">](http://dict.youdao.com/dictvoice?audio=access&type=2)&nbsp;&nbsp;[<img src="audio2.png" width="24">](https://audio00.forvo.com/audios/mp3/1/p/1p_8975595_39_283368_36283.mp3) | 存取，访问 | `/'æksɛs/` 注意重音 |"""

def convert_to_json(result):
    word, audios, meaning, symbol_tip = result
    elem = {}
    elem['id'] = str(uuid.uuid4())
    elem['word'] = word.lower()
    elem['meaning'] = {
        'zh-cn': meaning
    }
    elem['audio'] = {
        'usa': parse_audio(audios)[0],
        'us': parse_audio(audios)[1]
    }
    elem['tip'] = {}
    elem['symbol'], elem['tip']['zh-cn'] = parse_symbol_tip(symbol_tip)
    # return json.dumps(elem)
    return json.dumps(elem, ensure_ascii=False)

def parse_audio(audio_text):
    text_list = re.findall(r'\((.*?)\)', audio_text)
    if len(text_list) == 1:
        return text_list[0], ""
    else:
        return text_list

def parse_symbol_tip(symbol_text):
    text_list = symbol_text.split(" ", 1)
    if len(text_list) < 2:
        symbol = text_list[0]
        tip = ""
    else:
        symbol, tip = text_list
    return symbol[1: -1], tip

def parse(line):
    # print(line)
    result = list(
        filter(
            lambda x: x != "",
            list(map(
                lambda x: x.strip(),
                line.split("|")
            )) )
    )
    return convert_to_json(result)


# print(parse(test_line).encode('utf8').decode())
# print("\u5b58\u53d6\uff0c\u8bbf\u95ee")

def fetch_online_text(url):
    res = requests.get(url)
    parse_out = []
    for line in res.text.splitlines():
        if re.match(r"\| [a-zA-Z]", line):
            # pprint.pprint(parse(line))
            # break
            parse_out.append(parse(line))
    print("{\"words\": " + f"[{','.join(parse_out)}]" + "}")


fetch_online_text("https://raw.githubusercontent.com/jnoodle/common-programming-words-english-pronunciation/master/README.md")
