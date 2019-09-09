from use_example import ipproxy, ip





import requests

ok = 0
bad = 0

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'none',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
}

for asa in range(5000):
    c = ip.acquire_proxy()
    print(c)
    try:
        proxies = {
            "http": "http://{}".format(c),
            "https": "https://{}".format(c)
        }
        print(proxies)
        response = requests.get('https://www.baidu,com',headers=headers, proxies=proxies,timeout=1)
        if response.status_code == 200:

            print("____________")
            ok += 1
        else:
            print("AAAAAAAAAAAA")
            ip.delete_proxy(c)

            bad += 1
    except Exception:
        ip.delete_proxy(c)
        bad += 1

print(ok)
print(bad)