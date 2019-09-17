#!/usr/bin/env python3.7

import argparse
import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--name", dest="name", metavar="\"account name\"", help="name of the account to clone")

ARGS = PARSER.parse_args()

def run_clone(name):
    url = "https://github.com/" + name + "?tab=repositories"
    print("parsing",url)
    
    # get page
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError:
        sys.exit("Connection Error")
    soup = BeautifulSoup(page.text, "html.parser")
    
    # extract repo's names
    links = []
    for link in soup.find_all(itemprop="name codeRepository"):
        links.append(link.get("href"))
    print("found " + str(len(links)) + " repository")

    # make dir and clone repos
    try:
        os.mkdir(name)
    except FileExistsError:
        sys.exit("directory " + name + " already exists")

    os.chdir(name)

    for link in links:
        print(link)
        subprocess.run(["git","clone","https://github.com"+link+".git"])
    
    print("END")

if __name__ == '__main__':
    if ARGS.name is not None:
        run_clone(ARGS.name)
    else:
        sys.exit("no parameter --name provided, exiting.")
