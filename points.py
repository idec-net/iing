#!/usr/bin/env python3

import hashlib, random

def check_point(auth):
    points = open("points.txt", "r").read().split("\n")
    for i, n in enumerate(points):
        ud = n.split(":")
        if auth == ud[0]:
            return ud[1], i + 1
    return "", None

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def salt():
    return str(random.randint(1, 999999999))

def save_point(phash, user):
    open("points.txt", "a").write("%s:%s\n" % (phash, user))

if __name__ == "__main__":
    import sys
    user = "".join(sys.argv[1:])
    if user:
        phash = sha(user+salt())
        save_point(phash, user)
        print("Username: %s" % user)
        print("Authstr:  %s" % phash)
    else:
        print("Usage: points.py username.")
