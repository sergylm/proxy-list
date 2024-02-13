import requests
import json

def append_proxies(proxies, file):
    with open(file, "a") as f:
        for p in proxies:
            f.write("{}:{}\n".format(p["ip"],p["port"]))

def get_response(url):
    res = requests.get(url)
    return json.loads(res.content)

def get_geonode(params, nProxy = 100):
    page = 1
    file = "proxy_list.txt"
    while nProxy > 500:
        url = "https://proxylist.geonode.com/api/proxy-list?protocols={}&limit=500&page={}&sort_by=lastChecked&sort_type=desc".format("%2C".join(x.lower() for x in params), page)
        proxies = get_response(url)
        append_proxies(proxies["data"], file)
        nProxy -= 500
        page += 1
    
    url = "https://proxylist.geonode.com/api/proxy-list?protocols={}&limit={}&page={}&sort_by=lastChecked&sort_type=desc".format("%2C".join(x.lower() for x in params), nProxy, page)
    proxies = get_response(url)
    append_proxies(proxies["data"], file)
    pass


if __name__ == '__main__':
    params = ["HTTPS", "HTTPS", "SOCKS4", "SOCKS5"]
    nProxy = 1436
    get_geonode(params, nProxy)