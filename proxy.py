import requests
import json

def append_proxies(proxies, file):
    with open(file, "a") as f:
        for p in proxies:
            f.write("{}:{}\n".format(p["ip"],p["port"]))

def get_response(url):
    res = requests.get(url)
    return json.loads(res.content)

def get_geonode(protocols, nProxy):
    page = 1
    file = "proxy_list.txt"
    while nProxy > 500:
        url = "https://proxylist.geonode.com/api/proxy-list?protocols={}&limit=500&page={}&sort_by=lastChecked&sort_type=desc".format("%2C".join(protocols), page)
        proxies = get_response(url)
        append_proxies(proxies["data"], file)
        nProxy -= 500
        page += 1
    
    url = "https://proxylist.geonode.com/api/proxy-list?protocols=&limit={}&page={}&sort_by=lastChecked&sort_type=desc".format("%2C".join(protocols), nProxy, page)
    proxies = get_response(url)
    append_proxies(proxies["data"], file)
    pass

def get_proxyscape(protocols):
    if "https" in protocols:
        protocols.remove("https")
    if protocols is []:
        print("Proxyscape only supply HTTP, SOCKS4 and SOCKS5 proxies. Not HTTPS")
        return
    url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol={}&timeout=15000&proxy_format=ipport&format=json".format(",".join(protocols))
    proxies = get_response(url)
    append_proxies(proxies["proxies"], "proxyscrape_list.txt")
    # print(proxies["proxies"])

    pass


if __name__ == '__main__':
    protocols = ["http", "https", "socks4", "socks5"]
    nProxy = 1436
    # get_geonode(protocols, nProxy)
    get_proxyscape(protocols)