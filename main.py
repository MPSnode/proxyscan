import requests
from bs4 import BeautifulSoup
import concurrent.futures
import socks
import socket

# Function to fetch proxies from a website
def fetch_proxies(url):
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 1:
                ip = cols[0].text
                port = cols[1].text
                proxies.append(f"{ip}:{port}")
        return proxies
    except requests.exceptions.RequestException as e:
        print(f"Error fetching proxies from {url}: {e}")
        return []

# Function to check if a proxy is valid by making an actual HTTP request
def is_valid_proxy(proxy, proxy_type):
    try:
        if proxy_type == "HTTP":
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
            }
            response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        elif proxy_type == "SOCKS4":
            socks.set_default_proxy(socks.SOCKS4, proxy.split(':')[0], int(proxy.split(':')[1]))
            socket.socket = socks.socksocket
            response = requests.get("http://httpbin.org/ip", timeout=10)
        elif proxy_type == "SOCKS5":
            socks.set_default_proxy(socks.SOCKS5, proxy.split(':')[0], int(proxy.split(':')[1]))
            socket.socket = socks.socksocket
            response = requests.get("http://httpbin.org/ip", timeout=10)
        else:
            return proxy, False

        if response.status_code == 200:
            return proxy, True
    except:
        return proxy, False
    return proxy, False

# Function to print results with color coding
def print_result(proxy, is_valid):
    if is_valid:
        print(f"\033[92mIP: {proxy} - KET: VALID\033[0m")
    else:
        print(f"\033[91mIP: {proxy} - KET: NO VALID\033[0m")

# Main function
def main():
    proxy_sources = [
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://www.socks-proxy.net/',
        'https://www.proxy-list.download/HTTP',
        'https://www.proxy-list.download/HTTPS',
        'https://www.proxy-list.download/SOCKS4',
        'https://www.proxy-list.download/SOCKS5',
        'https://www.proxynova.com/proxy-server-list/',
        'https://www.proxynova.com/proxy-server-list/country-id/',
        'https://www.proxynova.com/proxy-server-list/country-us/',
        'https://www.proxynova.com/proxy-server-list/country-jp/',
        'https://www.proxynova.com/proxy-server-list/country-ru/',
        'https://www.proxynova.com/proxy-server-list/country-br/',
        'https://www.proxynova.com/proxy-server-list/country-cn/',
        'https://www.proxynova.com/proxy-server-list/country-de/',
        'https://www.proxynova.com/proxy-server-list/country-fr/',
        'https://www.proxynova.com/proxy-server-list/country-gb/',
        'https://www.proxynova.com/proxy-server-list/country-in/',
        'https://www.proxynova.com/proxy-server-list/country-it/',
        'https://www.proxynova.com/proxy-server-list/country-kr/',
        'https://www.proxynova.com/proxy-server-list/country-mx/',
        'https://www.proxynova.com/proxy-server-list/country-nl/',
        'https://www.proxynova.com/proxy-server-list/country-pl/',
        'https://www.proxynova.com/proxy-server-list/country-se/',
        'https://www.proxynova.com/proxy-server-list/country-th/',
        'https://www.proxynova.com/proxy-server-list/country-tr/',
        'https://www.proxynova.com/proxy-server-list/country-ua/',
        'https://www.proxynova.com/proxy-server-list/country-ve/',
        'https://www.proxynova.com/proxy-server-list/country-vn/',
        'https://www.proxy-list.org/english/search.php?search=ALL+LAST+REBOOTED',
        'https://www.proxy-list.org/english/search.php?search=ALL+LAST+RECONNECTED',
        'https://www.proxy-list.org/english/search.php?search=ALL+LAST+RELOADED',
        'https://www.proxy-list.org/english/search.php?search=ALL+LAST+RESTARTED',
        'https://www.proxy-list.org/english/search.php?search=ALL+LAST+REBOOTED',
        'https://www.proxy-list.org/english/search.php?search=ALL+LAST+RECONNECTED',
        'https://www.proxy-list.download/HTTP',
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://www.proxy-list.org/english/index.php',
        'https://www.proxynova.com/proxy-server-list/',
        'https://www.proxy-listen.de/Proxy/Proxyliste.html',
        'https://www.proxyscan.io/',
        'https://www.proxy-daily.com/',
        'https://www.geonode.com/free-proxy-list/',
        'https://www.proxy-list.download/SOCKS4',
        'https://www.socks-proxy.net/',
        'https://www.proxy-list.download/SOCKS5',
    ]

    all_proxies = []
    for url in proxy_sources:
        print(f"Fetching proxies from {url}")
        proxies = fetch_proxies(url)
        all_proxies.extend(proxies)

    valid_http_proxies = []
    valid_socks4_proxies = []
    valid_socks5_proxies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(is_valid_proxy, proxy, "HTTP"): proxy for proxy in all_proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy, is_valid = future.result()
            print_result(proxy, is_valid)
            if is_valid:
                valid_http_proxies.append(proxy)

        future_to_proxy = {executor.submit(is_valid_proxy, proxy, "SOCKS4"): proxy for proxy in all_proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy, is_valid = future.result()
            print_result(proxy, is_valid)
            if is_valid:
                valid_socks4_proxies.append(proxy)

        future_to_proxy = {executor.submit(is_valid_proxy, proxy, "SOCKS5"): proxy for proxy in all_proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy, is_valid = future.result()
            print_result(proxy, is_valid)
            if is_valid:
                valid_socks5_proxies.append(proxy)

    # Save valid proxies to separate files
    with open("valid_http_proxies.txt", "w") as file:
        for proxy in valid_http_proxies:
            file.write(f"{proxy}\n")

    with open("valid_socks4_proxies.txt", "w") as file:
        for proxy in valid_socks4_proxies:
            file.write(f"{proxy}\n")

    with open("valid_socks5_proxies.txt", "w") as file:
        for proxy in valid_socks5_proxies:
            file.write(f"{proxy}\n")

if __name__ == "__main__":
    main()