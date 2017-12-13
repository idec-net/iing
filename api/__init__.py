import os, re, time, math, codecs, base64, hashlib, sqlite3

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

def check_config():
    if not os.path.exists("iing.cfg"):
        open("iing.cfg", "w").write(open("iing.def.cfg", "r").read())

def init():
    if not os.path.exists("points.txt"):
        open("points.txt", "w").write("")
    if not os.path.exists("fecho"):
        os.makedirs("fecho")
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/indexes"):
        os.makedirs("files/indexes")
    if not os.path.exists("blacklist.txt"):
        open("blacklist.txt", "w")
    if not os.path.exists("fblacklist.txt"):
        open("fblacklist.txt", "w")
    if not os.path.exists("files/indexes/public_files.txt"):
        open("files/indexes/public_files.txt", "w")
    if not os.path.exists("files/indexes/files.txt"):
        open("files/indexes/files.txt", "w")
    if not os.path.exists("iing.cfg"):
        default_config = open("iing.def.cfg", "r").read()
        open("iing.cfg", "w").write(default_config)
    if not os.path.exists("points.txt"):
        open("points.txt", "w")

def load_config():
    global nodename, nodedsc, nodeurl, echoareas, fechoareas, shortareas, web_interface, background, norobots, registration, nosubscription
    nodename = ""
    nodedsc = ""
    nodeurl = ""
    background = []
    echoareas = []
    fechoareas = []
    shortareas = []
    web_interface = True
    norobots = False
    registration = False
    nosubscription = False

    cfg = codecs.open("iing.cfg", "r", "utf8").read().split("\n")
    for line in cfg:
        param = line.split(" ")
        if param[0] == "nodename":
            nodename = param[1]
        elif param[0] == "nodedsc":
            nodedsc = " ".join(param[1:])
        elif param[0] == "nodeurl":
            nodeurl = " ".join(param[1:])
        elif param[0] == "echo":
            echoareas.append([param[1], " ".join(param[2:])])
        elif param[0] == "fecho":
            fechoareas.append([param[1], " ".join(param[2:])])
        elif param[0] == "webinterface":
            if param[1] == "1":
                web_interface = True
            else:
                web_interface = False
        elif param[0] == "background":
            background = param[1].split(",")
        elif param[0] == "norobots":
            norobots = True
        elif param[0] == "registration":
            registration = True
        elif param[0] == "nosubscription":
            nosubscription = True

def get_echo_msgids(echo):
    msgids = []
    for row in c.execute("SELECT msgid FROM msg WHERE echoarea = ? ORDER BY id;", (echo,)):
        if len(row[0]) > 0:
            msgids.append(row[0])
    return msgids

def get_echoarea(echoarea):
    try:
        blacklist = open("blacklist.txt", "r").read().split("\n")
        result = []
        for msgid in get_echo_msgids(echoarea):
            if msgid != "" and not msgid in blacklist:
                result.append(msgid)
        return result
    except:
        return []

def get_msg(msgid):
    try:
        row = c.execute("SELECT tags, echoarea, time, fr, addr, t, subject, body FROM msg WHERE msgid = ?;", (msgid,)).fetchone()
        return "\n".join([row[0], row[1], str(row[2]), row[3], row[4], row[5], row[6], "", row[7]])
    except:
        return ""

def get_echoarea_count(echoarea):
    r = 0
    blacklist = open("blacklist.txt", "r").read().split("\n")
    q = c.execute("SELECT msgid FROM msg WHERE echoarea = ?;", (echoarea,))
    for row in q:
        if not row[0] in blacklist:
            r += 1
    return r

def get_last_msg(echoarea):
    try:
        row = c.execute("SELECT tags, echoarea, time, fr, addr, t, subject, body FROM msg WHERE echoarea = ? ORDER BY id DESC LIMIT 1;", (echoarea,)).fetchone()
        msg = [row[0], row[1], str(row[2]), row[3], row[4], row[5], row[6], row[7]]
    except:
        msg = []
    return msg

def get_last_msgid(echoarea):
    try:
        return c.execute("SELECT msgid FROM msg WHERE echoarea = ? ORDER BY id DESC LIMIT 1;", (echoarea,)).fetchone()[0]
    except:
        return False

def delete_msg(msgid):
    c.execute("DELETE FROM msg WHERE msgid = ?", (msgid,))
    con.commit()

def formatted_time(timestamp):
    return time.strftime("%d.%m.%y %H:%M UTC", time.gmtime(int(timestamp)))

def rss_time(timestamp):
    return time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime(int(timestamp)))

def get_time(echoarea):
    try:
        time = c.execute("SELECT time FROM msg WHERE echoarea = ? ORDER BY id DESC LIMIT 1;", (echoarea,)).fetchone()[0]
    except:
        time = 0
    return time

def echo_filter(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{1,60}\.[a-z0-9_!.-]{1,60}$')
    if rr.match(ea): return True

def fecho_filter(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{3,120}$')
    if rr.match(ea):
        return True
    else:
        return False

def msg_filter(msgid):
    rr = re.compile(r'^[a-z0-9A-Z]{20}$')
    if rr.match(msgid):
        return True
    else:
        return False

def file_filter(filename):
    rr = re.compile(r'^[A-Za-z0-9_!-.]{1,60}.[A-Za-z0-9_!-]{1,60}$')
    if rr.match(filename):
        return True
    else:
        return False

def hsh(msg):
    ret = base64.urlsafe_b64encode(hashlib.sha256(msg.encode()).digest()).decode("utf-8").replace("-", "A").replace("_", "z")[:20]
    return ret

def fhsh(msg):
    ret = base64.urlsafe_b64encode(hashlib.sha256(msg).digest()).decode("utf-8").replace("-", "A").replace("_", "z")[:20]
    return ret

def toss_msg(msgfrom, addr, tmsg):
    try:
        rawmsg = base64.b64decode(tmsg).decode("utf-8").split("\n")
        msg = []
        if rawmsg[4].startswith("@repto:"):
            msg.append("ii/ok/repto/" + rawmsg[4].split(":")[1])
            n = 5
        else:
            n = 4
            msg.append("ii/ok")
        echoarea = rawmsg[0]
        msg.append(rawmsg[0])
        msg.append(str(round(time.time())))
        msg.append(msgfrom)
        msg.append(nodename + "," + str(addr))
        msg.append(rawmsg[1])
        msg.append(rawmsg[2])
        msg.append("")
        for line in rawmsg[n:]:
            msg.append(line)
        msg = "\n".join(msg)
    except:
        msg = None
    if echo_filter(echoarea):
        if msg:
            if len(msg) <= 65535:
                h = hsh(msg)
                msg = msg.split("\n")
                c.execute("INSERT INTO msg (msgid, tags, echoarea, time, fr, addr, t, subject, body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (h, msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6], "\n".join(msg[8:])))
                con.commit()
                return "msg ok:" + h
            else:
                return "msg big!"
        else:
            return "error:unknown"
    else:
        return "incorrect echoarea"

def body_render(body):
    body = body.strip()
    body = body.replace("<", "&lt;").replace(">", "&gt;")
    rr = re.compile("((^|\n)[a-zA-Zа-яА-Я0-9_-]{0,20}(&gt;){1,20}.+)")
    body = rr.sub(r"<span class='quote'>\1</span>", body)
    rr = re.compile("((^|\n)(PS|P.S|ps|ЗЫ|З.Ы|\/\/|#).*)")
    body = rr.sub(r"\n<span class='comment'>\1</span>", body)
    rr = re.compile("((http|https|ftp):\/\/[a-z_0-9\-.:]+(\/[^ \t<>\n\r]+)?\/?)")
    body = rr.sub(r"<span class='url'><a target='_blank' href='\1'><i class='fa fa-link'></i> \1</a></span>", body)
    rr = re.compile("(ii:\/\/)([a-z0-9_!.-]{1,60}\.[a-z0-9_!.-]{1,59}[a-z0-9_!-])")
    body = rr.sub(r"<i class='fa fa-plane iilink'></i>&nbsp;<a class='iilink' href='\2'>\2</a>", body)
    rr = re.compile("(ii:\/\/)([a-z0-9A-Z]{20})")
    body = rr.sub(r"<i class='fa fa-envelope iilink'></i>&nbsp;<a class='iilink' href='\2'>\2</a>", body)
    rr = re.compile("((^|\n)(== ).+)")
    body = rr.sub(r"<h3 class='title'>\1</h3>", body)
    rr = re.compile("((^|\n)----)")
    body = rr.sub(r"<hr>", body)
    body = "<br>\n".join(body.split("\n"))
    txt = ""; pre = 0
    for line in body.split("\n"):
        if line.startswith("====") and pre == 0:
            pre = 1
            txt += "<pre>====\n"
        elif line.startswith("====") and pre == 1:
            pre = 0
            txt += "====</pre>\n"
        elif pre == 1:
            txt += line.replace("<br>", "") + "\n"
        else:
            txt += line + "\n"
    return txt

def get_file_size(filename):
    return os.stat("files/" + filename).st_size

def get_file_index(d):
    result = []
    files = codecs.open("files/indexes/files.txt", "r", "utf8").read().split("\n")
    fechoes = []
    dirs = []
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            try:
                size = str(get_file_size(fi[0]))
            except:
                size = "0"
            ff = fi[0].split("/")
            if d:
                if ff[0] == d:
                    result.append([ff[1], ff[0], size, " ".join(fi[1:]) + "\n"])
            else:
                if len(ff) > 1:
                    if not ff[0] in dirs:
                        dirs.append(ff[0])
                        result.append([ff[0] + "/", "", False, ""])
                else:
                    result.append([ff[0], "", size, " ".join(fi[1:]) + "\n"])
    return result

def get_public_file_index(d):
    result = []
    files = codecs.open("files/indexes/public_files.txt", "r", "utf8").read().split("\n")
    dirs = []
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            try:
                size = str(get_file_size(fi[0]))
            except:
                size = "0"
            ff = fi[0].split("/")
            if d:
                if ff[0] == d:
                    result.append([ff[1], ff[0], size, " ".join(fi[1:]) + "\n"])
            else:
                if len(ff) > 1:
                    if not ff[0] in dirs:
                        dirs.append(ff[0])
                        result.append([ff[0] + "/", "", False, ""])
                else:
                    result.append([ff[0], "", size, " ".join(fi[1:]) + "\n"])
    return result

def get_private_file_index(username, d):
    result = []
    files = codecs.open("files/indexes/" + username + "_files.txt", "r", "utf8").read().split("\n")
    dirs = []
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            try:
                size = str(get_file_size(fi[0]))
            except:
                size = "0"
            ff = fi[0].split("/")
            if d:
                if ff[0] == d:
                    result.append([ff[1], ff[0], size, " ".join(fi[1:]) + "\n"])
            else:
                if len(ff) > 1:
                    if not ff[0] in dirs:
                        dirs.append(ff[0])
                        result.append([ff[0] + "/", "", False, ""])
                else:
                    result.append([ff[0], "", size, " ".join(fi[1:]) + "\n"])
    return result

def get_fechoarea(fechoarea):
    result = []
    try:
        files = codecs.open("fecho/" + fechoarea, "r", "utf8").read().split("\n")
        for f in files:
            if len(f) > 0:
                fi = f.split(":")
                result.append([fi[0], ":".join(fi[1:])])
    except:
        None
    return result
