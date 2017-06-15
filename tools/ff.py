#!/usr/bin/env python3

import sys, requests, os

config = False
node = False
pauth = False
fecho = False
f = False
dsc = False

def load_config(filename):
    global node, pauth
    f = open(filename, "r").read().split("\n")
    for line in f:
        param = line.split(" ")
        if param[0] == "node":
            node = param[1]
        elif param[0] == "auth":
            pauth = " ".join(param[1:])

args = sys.argv[1:]
if "-c" in args:
    config = args[args.index("-c") + 1]
if "-e" in args:
    fecho = args[args.index("-e") + 1]
if "-f" in args:
    f = args[args.index("-f") + 1]
if "-d" in args:
    dsc = args[args.index("-d") + 1]

try:
    load_config(config)
except:
    None

if config and node and pauth and fecho and f and dsc:
    files = {"file": open(f, "rb")}
    data = {"pauth": pauth, "fecho": fecho, "dsc": dsc}
    print("Отправка файла %s." % os.path.basename(f), end=": ")
    try:
        r = requests.post(node + "f/p", data=data, files=files)
        print("OK")
    except:
        print("ERROR")
    print(r.text)
else:
    print("Usage: ff.py -c <config> -e <fileecho> -f <filename> -d <description>.")
    print()
    print("Config format:")
    print("node URL")
    print("auth authstr")
