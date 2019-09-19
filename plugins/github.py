#!/usr/bin/env python3.7

import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)


class Remote:
    links = []

    def __init__(self, username, target='.'):
        self.username = username
        self.target = target


    def get_list_repos(self):
        url = "https://github.com/" + self.username + "?tab=repositories"
        print(Fore.BLUE + Style.BRIGHT + "parsing",url)

        # get page
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError:
            sys.exit(Fore.RED + Style.BRIGHT + "Connection Error")
        soup = BeautifulSoup(page.text, "html.parser")

        # extract repo's names
        for link in soup.find_all(itemprop="name codeRepository"):
            self.links.append(link.get("href"))
        print(Fore.GREEN + Style.BRIGHT + "found " + str(len(self.links)) + " repository")


    def print_list_repos(self):
        print("repository list:")
        for i in range(0, len(self.links)-1):
            print(' '+str(i+1)+')'+self.links[i])


    def clone_repos(self, repos=[]):
        link_array = []
        if len(repos):
            for i in repos:
                try:
                    integer = int(i)
                except ValueError:
                    print(Fore.YELLOW + Style.BRIGHT + i+" not a number, skipped")
                    continue
                if integer < 0 or integer >= len(self.links):
                    print(Fore.YELLOW + Style.BRIGHT + i+" out of range, skipped")
                    continue
                link_array.append(self.links[integer-1])
        else:
            link_array = self.links

        if self.target[-1] is not '/':
            directory = self.target + '/' + self.username
        else:
            directory = self.target + self.username

        try:
            os.mkdir(directory)
        except FileExistsError:
            sys.exit(Fore.RED + Style.BRIGHT + "directory " + directory + " already exists")

        os.chdir(directory)

        for link in link_array:
            print(Fore.BLUE + Style.BRIGHT + "Start cloning: " + link.replace('/'+self.username+'/',''))
            subprocess.run(["git","clone","https://github.com"+link+".git"])

