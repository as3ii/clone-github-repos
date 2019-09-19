#!/usr/bin/env python3.7

import importlib
import argparse
import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)


# collect plugins
PLUGIN_LIST = []
for filename in os.listdir("plugins"):
    if ".py" in filename and "__" not in filename:
        PLUGIN_LIST.append("plugins."+filename.replace(".py",''))


PARSER = argparse.ArgumentParser()
PARSER.add_argument("-n", "--name", dest="name", metavar="\"account name\"", help="name of the account to clone")
PARSER.add_argument("-i", "--interatctive", dest="inter", action="store_true", help="exec script in interactive mode")
PARSER.add_argument("-t", "--target", dest="target", metavar="\"/destination/directory\"", help="target directory where to put the cloned repos")
PARSER.add_argument("-r", "--remote", dest="remote", metavar="github", help="remote repository server such as github or gitlab")
PARSER.set_defaults(name=None, inter=False, target='.', remote="github")

ARGS = PARSER.parse_args()


def run_script(name, target, remote):
    if remote not in PLUGIN_LIST:
        sys.exit(Fore.RED + Style.BRIGHT + "Plugin for this remote platform not found")
    plugin = importlib.import_module("plugins."+remote, '.')
    user = plugin.Remote(name, target)
    user.get_list_repos()
    user.clone_repos()
    print(Fore.BLUE + Style.BRIGHT + "END")


def run_interactive(name, target, remote):
    if remote is None:
        print("Remote repository platform: ",", ".join(PLUGIN_LIST))
        remote = input("Choose one of the listed platform: [default: github] ")
        if remote == '':
            remote = "github"
    if remote not in PLUGIN_LIST:
        sys.exit(Fore.RED + Style.BRIGHT + "Plugin for this remote platform not found")

    if name is None:
        name = input("Platform Username: ")

    plugin = importlib.import_module("plugins."+remote, '.')
    user = plugin.Remote(name)
    user.get_list_repos()
    user.print_list_repos()

    repo_str = input("Write which repo to download (space-separated or \"all\") [1-"+str(len(user.links))+"]: ")
    if repo_str.lower() == "all":
        repo_list = range(len(links))
    else:
        repo_list = repo_str.split(' ')

    if target == '.':
        user.target = input("Target directory (press enter to default): ")
        if user.target == '':
            user.target = '.'

    user.clone_repos(repo_list)
    print(Fore.BLUE + Style.BRIGHT + "END")


if __name__ == '__main__':
    try:
        if ARGS.inter:
            run_interactive(ARGS.name, ARGS.target, ARGS.remote)
        elif ARGS.name is not None and ARGS.target is not None and ARGS.remote:
            run_script(ARGS.name, ARGS.target, ARGS.remote)
        else:
            sys.exit(Fore.RED + Style.BRIGHT + "not enough parameter provided, exiting.")
    except KeyboardInterrupt:
        sys.exit(Fore.RED + Style.BRIGHT + "\nKeyboard Interrupt received, exiting.")

