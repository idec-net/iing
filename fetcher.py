#!/usr/bin/env python3

import urllib.request, base64, codecs, re, os, sys, pickle, sqlite3

con = sqlite3.connect("idec.db")
c = con.cursor()

# Create databse
c.execute("""CREATE TABLE IF NOT EXISTS msg(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    msgid TEXT,
    tags TEXT,
    echoarea TEXT,
    time INTEGER,
    fr TEXT,
    addr TEXT,
    t TEXT,
    subject TEXT,
    body TEXT,
    UNIQUE (id));""")
c.execute("CREATE INDEX IF NOT EXISTS msgid ON 'msg' ('msgid');")
c.execute("CREATE INDEX IF NOT EXISTS echoarea ON 'msg' ('echoarea');")
c.execute("CREATE INDEX IF NOT EXISTS time ON 'msg' ('time');")
c.execute("CREATE INDEX IF NOT EXISTS subject ON 'msg' ('subject');")
c.execute("CREATE INDEX IF NOT EXISTS body ON 'msg' ('body');")
con.commit()

clone = []
counts = {}
remote_counts = {}
full = False
h = False
features = []
ue = False
xc = False
to = False
depth = "200"

def load_config():
    auth = ""
    node = ""
    depth = "200"
    echoareas = []
    fechoareas = []
    f = open(config, "r").read().split("\n")
    for line in f:
        param = line.split(" ")
        if param[0] == "node":
            node = param[1]
        elif param[0] == "depth":
            depth = param[1]
        elif param[0] == "echo":
            echoareas.append(param[1])
        elif param[0] == "fecho":
            fechoareas.append(param[1])
    return node, depth, echoareas, fechoareas

def check_directories():
    if not os.path.exists("fecho"):
        os.makedirs("fecho")
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/indexes"):
        os.makedirs("files/indexes")

def separate(l, step=40):
    for x in range(0, len(l), step):
        yield l[x:x+step]

def get_features():
    global features
    try:
        r = urllib.request.Request(node + "x/features")
        with urllib.request.urlopen(r) as f:
            features = f.read().decode("utf-8").split("\n")
    except:
        features = []

def check_features():
    global ue, xc
    ue = "u/e" in features
    xc = "x/c" in features

def load_counts():
    global counts
    if os.path.exists("counts.lst"):
        f = open("counts.lst", "rb")
        counts = pickle.load(f)
        f.close()
    else:
        counts[node] = {}
    if not node in counts:
        counts[node] = {}

def save_counts():
    counts[node] = remote_counts
    f = open("counts.lst", "wb")
    pickle.dump(counts, f)
    f.close()

def get_remote_counts():
    counts = {}
    r = urllib.request.Request(node + "x/c/" + "/".join(echoareas))
    with urllib.request.urlopen(r) as f:
        c = f.read().decode("utf-8").split("\n")
    for count in c:
        echoarea = count.split(":")
        if len(echoarea) > 1:
            counts[echoarea[0]] = echoarea[1]
    return counts

def calculate_offset():
    global depth
    n = False
    offset = 0
    for echoarea in echoareas:
        if not echoarea in counts[node]:
            n = True
        else:
            if not echoarea in clone and int(remote_counts[echoarea]) - int(counts[node][echoarea]) > offset:
                offset = int(remote_counts[echoarea]) - int(counts[node][echoarea])
    if not n:
        depth = offset

def get_echoarea(echo):
    msgids = []
    for row in c.execute("SELECT msgid FROM msg WHERE echoarea = ? ORDER BY id;", (echo,)):
        if len(row[0]) > 0:
            msgids.append(row[0])
    return msgids

def get_msg_list():
    global clone
    msg_list = []
    fetch_echoareas = []
    if not full and ue:
        for echoarea in echoareas:
            if not echoarea in clone and (not echoarea in counts[node] or int(counts[node][echoarea]) < int(remote_counts[echoarea])):
                fetch_echoareas.append(echoarea)
    else:

        clone = echoareas
    if len(clone) > 0:
        r = urllib.request.Request(node + "u/e/" + "/".join(clone))
        with urllib.request.urlopen(r) as f:
            lines = f.read().decode("utf-8").split("\n")
            for line in lines:
                if len(line) > 0:
                    msg_list.append(line)
    if len(fetch_echoareas) > 0 and int(depth) > 0:
        r = urllib.request.Request(node + "u/e/" + "/".join(fetch_echoareas) + "/-%s:%s" %(depth, depth))
        with urllib.request.urlopen(r) as f:
            lines = f.read().decode("utf-8").split("\n")
            for line in lines:
                if len(line) > 0:
                    msg_list.append(line)
    return msg_list

def get_bundle(node, msgids):
    bundle = []
    r = urllib.request.Request(node + "u/m/" + msgids)
    with urllib.request.urlopen(r) as f:
        bundle = f.read().decode("utf-8").split("\n")
    return bundle

def debundle(bundle):
    for msg in bundle:
        if msg:
            m = msg.split(":")
            msgid = m[0]
            if len(msgid) == 20 and m[1]:
                msg = base64.b64decode(m[1].encode("ascii")).decode("utf8").split("\n")
                c.execute("INSERT INTO msg (msgid, tags, echoarea, time, fr, addr, t, subject, body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (msgid, msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6], "\n".join(msg[7:])))
    con.commit()

def echo_filter(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{1,60}\.[a-z0-9_!.-]{1,60}$')
    if rr.match(ea): return True

def get_mail():
    fetch_msg_list = []
    print("Получение индекса от ноды...")
    local_index = []
    remote_msg_list = get_msg_list()
    print("Построение разностного индекса...")
    for line in remote_msg_list:
        if echo_filter(line):
            if line in clone or full:
                try:
                    c.execute("DELETE FROM msg WHERE echoarea = ?;", (line,))
                    con.commit
                except:
                    None
            local_index = get_echoarea(line)
        else:
            if not line in local_index:
                fetch_msg_list.append(line)
    msg_list_len = str(len(fetch_msg_list))
    if len(fetch_msg_list) > 0:
        count = 0
        for get_list in separate(fetch_msg_list):
            count = count + len(get_list)
            print("\rПолучение сообщений: " + str(count) + "/"  + msg_list_len, end="")
            debundle(get_bundle(node, "/".join(get_list)))
    else:
        print("Новых сообщений не обнаружено.", end="")
    print()

def get_local_fecho(fecho):
    index = []
    try:
        for f in open("fecho/%s" % fecho, "r").read().split("\n"):
            if len(f) > 0:
                index.append(f)
    except:
        None
    return index

def get_remote_fecho():
    index = []
    try:
        r = urllib.request.Request(node + "f/e/" + "/".join(fechoareas))
        with urllib.request.urlopen(r) as f:
            for row in f.read().decode("utf8").split("\n"):
                if len(row) > 0:
                    index.append(row)
    except:
        None
    return index

def download_file(fi):
    r = urllib.request.Request("%sf/f/%s/%s" % (node, fi[0], fi[1].split(":")[0]))
    out = urllib.request.urlopen(r)
    file_size=0
    block_size=8192

    if not os.path.exists("files/%s" % fi[0]):
        os.mkdir("files/%s" % fi[0])
    f = open("files/%s/%s" % (fi[0], fi[1].split(":")[1]), "wb")
    while True:
        buffer = out.read(block_size)
        if not buffer:
            break
        file_size += len(buffer)
        f.write(buffer)
    f.close()
    codecs.open("fecho/%s" % fi[0], "a", "utf-8").write(fi[1] + "\n")
    fe = fi[0]
    fi = fi[1].split(":")
    codecs.open("files/indexes/files.txt", "a", "utf-8").write(fe + "/" + fi[1] + ":" + ":".join(fi[4:]) + "\n")

def get_fecho():
    print("Получение индекса файлэх.")
    remote_index = get_remote_fecho()
    print("Построение разностного индекса.")
    local_index = []
    for fecho in fechoareas:
        local_fecho = get_local_fecho(fecho)
        for fid in local_fecho:
            local_index.append(fid)
    index = []
    for fi in remote_index:
        if not ":" in fi:
            fecho = fi
        elif not fi in local_index:
            index.append([fecho, fi])
    for fi in index:
        row = fi[1].split(":")
        print("Получение файла %s" % row[1], end=" ")
        try:
            download_file(fi)
            print("OK")
        except:
            print("ERROR")

def check_new_echoareas():
    local_base = []
    for row in c.execute("SELECT echoarea FROM msg GROUP BY echoarea;"):
        local_base.append(row[0])
    n = False
    for echoarea in echoareas:
        if not echoarea in local_base:
            n = True
    return n

def show_help():
    print("Usage: fetcher.py [-f filename] [-n node] [-e echoarea1,echoarea2,...] [-d depth] [-c echoarea1,echoarea2,...] [-o] [-to name1,name2...] [-h].")
    print()
    print("  -f filename  load config file. Default idec-fetcher.cfg.")
    print("  -n node      node address.")
    print("  -e echoareas echoareas for fetch.")
    print("  -d depth     fetch messages with an offset to a predetermined depth. Default 200.")
    print("  -c echoareas clone echoareas from node.")
    print("  -o           old mode. Get full index from nore.")
    print("  -to names    names for put messages to carbonarea.")
    print("  -h           this message.")
    print()
    print("If -f not exist, script will load config from current directory with name\nfetcher.cfg.")

args = sys.argv[1:]

conf = "-f" in args
if conf:
    config = args[args.index("-f") + 1]
else:
    config = "fetcher.cfg"
if "-c" in args:
    clone = args[args.index("-c") + 1].split(",")
full = "-o" in args
if "-d" in args:
    depth = args[args.index("-d") + 1]
h = "-h" in args
if "-n" in args:
    node = args[args.index("-n") + 1]
if "-e" in args:
    echoareas = args[args.index("-e") + 1].split(",")
if "-to" in args:
    to = args[args.index("-to") + 1].split(",")
wait = "-w" in args

if h:
    show_help()
    quit()

if not "-n" in args and not "-e" in args and not os.path.exists(config):
    print("Config file not found.")
    quit()

check_directories()
if not "-n" in args or not "-e" in args:
    node, depth, echoareas, fechoareas = load_config()
print("Работа с " + node)
print("Получение списка возможностей ноды...")
get_features()
check_features()
if len(echoareas) > 0 and xc and not full:
    load_counts()
    print("Получение количества сообщений в конференциях...")
    remote_counts = get_remote_counts()
    calculate_offset()
get_mail()
get_fecho()
if xc:
    save_counts()
if wait:
    input("Нажмите Enter для продолжения.")
    print()
