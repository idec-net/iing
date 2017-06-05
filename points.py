#!/usr/bin/env python3

import hashlib, random, base64

def check_point(auth):
    try:
        points = open("points.txt", "r").read().split("\n")
        for i, n in enumerate(points):
            ud = n.split(":")
            if auth == ud[1]:
                return ud[2], i + 1
        return "", None
    except:
        return "", None

def login(user, password):
    try:
        points = open("points.txt", "r").read().split("\n")
        for i, n in enumerate(points):
            ud = n.split(":")
            if len(ud) == 3 and hsh(user.encode("utf-8") + password.encode("utf-8")) == ud[0]:
                return ud[1]
        return "error"
    except:
        return False

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def salt():
    return str(random.randint(1, 999999999))

def hsh(str):
    return base64.urlsafe_b64encode(hashlib.sha256(str).digest()).decode("utf-8")

def save_point(phash, user, hsh):
    open("points.txt", "a").write("%s:%s:%s\n" % (hsh, phash, user))

def make_point(user, password):
    hs = hsh(user.encode("utf-8") + password.encode("utf-8"))
    phash = sha(user+salt())
    return hs, phash

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if "-u" in args and "-p":
        user = args[args.index("-u") + 1]
        password = args[args.index("-p") + 1]
        hsh, phash = make_point(user, password)
        save_point(phash, user, hsh)
        print("Username: %s" % user)
        print("Password: %s" % password)
        print("Authstr:  %s" % phash)
    else:
        print("Usage: points.py -u username -p password.")
