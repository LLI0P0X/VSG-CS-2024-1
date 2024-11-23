import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'PHPSESSID=c348082492ac0719a9c243810872880f; _ym_uid=1732285071523628253; _ym_d=1732285071; _ym_isad=2',
    'origin': 'https://snipp.ru',
    'priority': 'u=0, i',
    'referer': 'https://snipp.ru/tools/ip',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5", "YaBrowserCorp";v="126.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
}

data = {
    'ip': '193.41.142.172',
    'send': 'Отправить',
}

response = requests.post('https://snipp.ru/tools/ip', headers=headers, data=data, verify=False)

f = open('temp.html', 'w', encoding='utf-8')
f.write(response.text)
f.write(response.text)
f.close()


