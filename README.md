# Proxy Validator Script

This script fetches proxy lists from various sources, validates them by making actual HTTP requests, and saves the valid proxies to a text file. It uses multithreading to speed up the validation process.

## Features

- Fetches proxies from multiple sources.
- Validates proxies by making actual HTTP requests.
- Uses multithreading for fast scanning.
- Saves valid proxies to a text file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:

    ```sh
    pip install requests beautifulsoup4
    ```

## Usage

1. Run the script using the following command:

    ```sh
    python proxy.py
    ```

2. The script will fetch proxies from various sources, validate them, and save the valid proxies to a file named `valid_proxies.txt`.

## Example

Here is an example of the output:

```plaintext
Fetching proxies from https://www.sslproxies.org/
IP: 104.156.140.145:3128 - KET: VALID
IP: 108.170.12.11:80 - KET: NO VALID
IP: 157.245.95.247:443 - KET: VALID
IP: 149.129.255.179:8081 - KET: NO VALID
IP: 8.148.4.166:3128 - KET: VALID