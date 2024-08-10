import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Function to fetch proxies from a website
def fetch_proxies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"{ip}:{port}")
    return proxies

# Function to check if a proxy is valid by making an actual HTTP request
def is_valid_proxy(proxy):
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
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
    ]

    all_proxies = []
    for url in proxy_sources:
        print(f"Fetching proxies from {url}")
        proxies = fetch_proxies(url)
        all_proxies.extend(proxies)

    valid_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(is_valid_proxy, proxy): proxy for proxy in all_proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy, is_valid = future.result()
            print_result(proxy, is_valid)
            if is_valid:
                valid_proxies.append(proxy)

    # Save valid proxies to a file
    with open("valid_proxies.txt", "w") as file:
        for proxy in valid_proxies:
            file.write(f"{proxy}\n")

if __name__ == "__main__":
    main()