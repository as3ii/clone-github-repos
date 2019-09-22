import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)


class Remote:
    repo_names = []

    def __init__(self, username, target='.'):
        self.username = username
        self.target = target


    def get_list_repos(self):
        url = f"https://github.com/{self.username}?tab=repositories"
        print(f"{Fore.BLUE}{Style.BRIGHT}Parsing {url}")

        # get page
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError:
            sys.exit(f"{Fore.RED}{Style.BRIGHT}Connection Error")
        soup = BeautifulSoup(page.text, "html.parser")

        # extract repo's names
        for repos in soup.find_all(itemprop="name codeRepository"):
            self.repo_names.append(repos.get("href").replace(f"/{self.username}/",''))
        print(f"{Fore.GREEN}{Style.BRIGHT}Found {str(len(self.repo_names))} repository")


    def print_list_repos(self):
        print("Repository list:")
        for i in range(0, len(self.repo_names)-1):
            print(f" {str(i+1)}) {self.repo_names[i]}")


    def clone_repos(self, repos=[]):
        repo_array = []
        if len(repos):
            for i in repos:
                try:
                    integer = int(i)
                except ValueError:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}{i} not a number, skipped")
                    continue
                if integer < 0 or integer >= len(self.links):
                    print(f"{Fore.YELLOW}{Style.BRIGHT}{i} out of range, skipped")
                    continue
                repo_array.append(self.repo_names[integer-1])
        else:
            repo_array = self.repo_names

        if self.target[-1] is not '/':
            directory = self.target + '/' + self.username
        else:
            directory = self.target + self.username

        try:
            os.mkdir(directory)
        except FileExistsError:
            sys.exit(f"{Fore.RED}{Style.BRIGHT}Directory {directory} already exists")

        os.chdir(directory)

        for repo in repo_array:
            print(f"{Fore.BLUE}{Style.BRIGHT}Start cloning: {repo}")
            subprocess.run(["git","clone",f"https://github.com/{self.username}/{repo}.git"])

