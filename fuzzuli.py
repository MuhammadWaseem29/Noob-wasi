import argparse
import requests
import concurrent.futures
import time
import re
import os

# ANSI escape codes for colors
GREEN = "\033[32m"
RESET = "\033[0m"

# Global variables
urls = []
methods = []
extensions = [".rar", ".zip", ".tar.gz", ".tar", ".gz", ".jar", ".7z", ".bz2", ".sql", ".backup", ".war", ".bak", ".dll"]
mime_types = [
    "application/octet-stream",
    "application/x-bzip",
    "application/x-bzip2",
    "application/gzip",
    "application/java-archive",
    "application/vnd.rar",
    "application/x-sh",
    "application/x-tar",
    "application/zip",
    "application/x-7z-compressed",
    "application/x-msdownload",
    "application/x-msdos-program",
]

def parse_options():
    parser = argparse.ArgumentParser(description='Noob-Wasi: A URL fuzzing tool created by Muhammad Waseem to find critical backup files by creating a dynamic wordlist based on the domain.')
    
    # Input Flags
    parser.add_argument('-d', '--domain', help='Domain to find backup files for.')
    parser.add_argument('-f', '--file', help='Input file containing list of domains (one per line).')
    
    # Path Flags
    parser.add_argument('-pt', '--paths', default='/', help='Paths to scan. Separate with commas for multiple paths (e.g. /,/db/,/old/).')
    
    # Method Flags
    parser.add_argument('-mt', '--method', help='Methods for generating wordlists (e.g. regular, withoutdots, withoutvowels).')
    
    # Extension Flags
    parser.add_argument('-ex', '--extension', help='File extensions to search for (e.g. .zip,.tar).')
    
    # Output Flags
    parser.add_argument('-o', '--output', help='File to write output results to.')
    parser.add_argument('-p', '--print', action='store_true', help='Print URLs that are sent requests.')
    
    # Misc Flags
    parser.add_argument('-sl', '--silent', action='store_true', help='Silent mode, suppress output.')
    parser.add_argument('-jw', '--just_wordlist', action='store_true', help='Just generate wordlist, do not make HTTP requests.')
    parser.add_argument('-t', '--tags', help='Comma-separated list of tags to filter wordlists.')
    
    return parser.parse_args()

def read_from_file(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f.readlines()]

def generate_wordlist(domain):
    wordlist = []
    if options.tags:
        tags = options.tags.split(',')
        for tag in tags:
            wordlist.append(f"{domain}/{tag}")
            wordlist.append(f"{domain}/backup_{tag}")
            wordlist.append(f"{domain}/old_{tag}")
    else:
        wordlist.append(f"{domain}/backup")
        wordlist.append(f"{domain}/old")
    
    return wordlist

def head_request(domain, word):
    for e in extensions:
        for path in paths:
            url = f"{domain}{path}{word}{e}"
            if options.print:
                print(f"{GREEN}[-] {url}{RESET}")
            try:
                response = requests.head(url)
                if response.status_code == 200:
                    print(f"{GREEN}[+] Found: {url}{RESET}")
            except requests.RequestException:
                continue

def banner():
    print("\n" + "="*30)
    print(f"{GREEN}       Noob-Wasi{RESET}")
    print(f"{GREEN} Created by Muhammad Waseem{RESET}")
    print("="*30 + "\n")

def main():
    global options
    options = parse_options()
    banner()  # Display the banner

    if options.file:
        urls.extend(read_from_file(options.file))
    elif options.domain:
        urls.append(options.domain)
    else:
        print("[!] No input provided. Use -d or -f.")
        return

    if options.extension:
        global extensions
        extensions = options.extension.split(',')

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        for url in urls:
            wordlist = generate_wordlist(url)
            for word in wordlist:
                executor.submit(head_request, url, word)

if __name__ == "__main__":
    main()
