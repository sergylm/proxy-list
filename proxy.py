import requests
import json

import argparse
from argparse import RawTextHelpFormatter

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

def get_free_proxy(protocols):
    if "socks4" in protocols or "socks5" in protocols:
        print("free-proxy-list only sypply HTTP an HTTPS")
        
    url = "https://free-proxy-list.net/"
    res = requests.get(url)
    proxies = parse_free_proxy(res.text)

    append_proxies(proxies, "free_proxy.txt")

def parse_free_proxy(res):
    proxies = []
    res = res.split('onclick="select(this)">')[1]
    res = res.split('</textarea>')[0]
    res = res.split("\n")[3:-1]
    for x in res:
        ip, port = x.split(":")
        proxies.append({"ip" : ip, "port" : port})
    return proxies
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gather proxies from several providers.\nSelect type proxy within http, https, socks4 and socks5.\nSpecify number of proxies.',
    epilog= "Examples:\n\
    Gather only socks4 and socks5 proxies:\n\
        proxy.py --type socks4 socks4\n\
    Gather 10 proxies\n\
        proxy.py -n 10\n\
    Gather 15 proxies of type socks5\n\
        proxy.py -n --type socks5", formatter_class=RawTextHelpFormatter)
    parser.add_argument('--type' , nargs='*', metavar="TYPE", help='Specify proxy type separate by commas. (Default: http https).', choices=['http', 'https', 'socks4', 'socks5'], default=['http','https'], dest='type')
    parser.add_argument('--list', help='Display list of available providers.', dest='list', action='store_false')
    parser.add_argument('-n', type=int, metavar="N", help='Number of proxies gather. (Default: 1).', default=1)
    args = parser.parse_args()
   