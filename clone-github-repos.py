#!/usr/bin/env python3.7

import argparse
import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup


PARSER = argparse.ArgumentParser()
PARSER.add_argument("-n", "--name", dest="name", metavar="\"account name\"", help="name of the account to clone")
PARSER.add_argument("-i", "--interatctive", dest="inter", action="store_true", help="exec script in interactive mode")
PARSER.add_argument("-t", "--target", dest="target", metavar="\"/destination/directory\"", help="target directory where to put the cloned repos")
PARSER.set_defaults(name=None, inter=False, target=None)

ARGS = PARSER.parse_args()


def extract_repos_list(name):
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
    return(links)


def clone(links, target, name):
    if target[-1] is not '/':
        directory = target + '/' + name
    else:
        directory = target + name

    try:
        os.mkdir(directory)
    except FileExistsError:
        sys.exit("directory " + directory + " already exists")

    os.chdir(directory)

    for link in links:
        print(link.replace('/'+name+'/',''))
        subprocess.run(["git","clone","https://github.com"+link+".git"])


def run_script(name, target):
    links = extract_repos_list(name)
    clone(links, target, name)


def run_interactive():
    name = input("Github Username: ")
    links = extract_repos_list(name)
    if len(links) == 0:
        sys.exit("no repository found")
    print("repository list:")
    for i in range(0, len(links)-1):
        print(' '+str(i+1)+')'+links[i])
    repo_str = input("Write which repo to download (space-separated or \"all\") [1-"+str(len(links))+"]: ")
    if repo_str.lower() == "all":
        repo_list = range(len(links))
    else:
        repo_list = repo_str.split(' ')
    array = []
    for i in repo_list:
        try:
            integer = int(i)
        except ValueError:
            print(i+" not a number, skipped")
            continue
        if integer < 0 or integer > len(links):
            print(i+" out of range, skipped")
            continue
        array.append(links[integer-1])

    target = input("Target directory: ")
    clone(array, target, name)
    print("END")


if __name__ == '__main__':
    try:
        if ARGS.inter:
            run_interactive()
        elif ARGS.name is not None and ARGS.target is not None:
            run_script(ARGS.name, ARGS.target)
        else:
            sys.exit("not enough parameter provided, exiting.")
    except KeyboardInterrupt:
        sys.exit("\nKeyboard Interrupt received, exiting.")

