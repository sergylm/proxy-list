import requests

valid_proxies = []

def check_proxies():
    global valid_proxies
    with open("proxy_list.txt", "r") as f:
        proxies = f.read().split("\n")
        for p in proxies:
            try:
                res = requests.get("http://ifconfig.me", proxies={"http": p, "https": p}, timeout = 10)
            except:
                continue
            if res.status_code == 200:
                print("Validating proxies {}".format(len(valid_proxies)),end="\r", flush=True)
                valid_proxies.append(proxy)
    
    with open("valid_proxy_list.txt", "w") as f:
        f.write("\n".join(valid_proxies))    