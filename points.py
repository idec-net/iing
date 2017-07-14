#!/usr/bin/env python3

import hashlib, random, base64

def check_point(auth):
    try:
        points = open("points.txt", "r").read().split("\n")
        for n in points:
            ud = n.split(":")
            if auth == ud[1]:
                return ud[2], ud[3]
        return "", None
    except:
        return "", None

def check_username(username):
    points = open("points.txt", "r").read().split("\n")
    for n in points:
        if len(n) > 0:
            ud = n.split(":")
            if username == ud[2]:
                return True
    return False

def login(user, password):
    try:
        points = open("points.txt", "r").read().split("\n")
        for i, n in enumerate(points):
            ud = n.split(":")
            if len(ud) == 4 and hsh(user.encode("utf-8") + password.encode("utf-8")) == ud[0]:
                return ud[1]
        return "error"
    except:
        return False

def is_operator(auth):
    points = open("points.txt", "r").read().split("\n")
    for point in points:
        row = point.split(":")
        if len(row) > 4 and auth == row[1]:
            flags = row[4].split(",")
            if "OP" in flags:
                return True
    return False

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def salt():
    return str(random.randint(1, 999999999))

def hsh(str):
    out = base64.urlsafe_b64encode(hashlib.sha256(str).digest()).decode("utf-8")
    return out.replace('-', '').replace('_', '')[:8].ljust(8,'A')

def save_point(phash, user, hsh):
    addrs = []
    m = 0
    for point in open("points.txt", "r").read().split("\n"):
        if len(point) > 0:
            m += 1
            row = point.split(":")
            addrs.append(int(row[3]))
    for i in range(1, m + 2):
        if not i in addrs:
            point = i
            break
    open("points.txt", "a").write("%s:%s:%s:%s\n" % (hsh, phash, user, point))

def make_point(user, password):
    hs = hsh(user.encode("utf-8") + password.encode("utf-8"))
    phash = sha(user+salt())
    return hs, phash

if __name__ == "__main__":
    import sys, os
    if not os.path.exists("points.txt"):
        open("points.txt", "w").write("")
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
