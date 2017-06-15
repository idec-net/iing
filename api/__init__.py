import os, re, time, math, codecs, base64, hashlib

def init():
    if not os.path.exists("echo"):
        os.makedirs("echo")
    if not os.path.exists("msg"):
        os.makedirs("msg")
    if not os.path.exists("fecho"):
        os.makedirs("fecho")
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/indexes"):
        os.makedirs("files/indexes")
    if not os.path.exists("blacklist.txt"):
        open("blacklist.txt", "w")
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
    global nodename, nodedsc, echoareas, shortareas, web_interface, background, norobots, registration
    nodename = ""
    nodedsc = ""
    background = []
    echoareas = []
    shortareas = []
    web_interface = True
    norobots = False
    registration = False

    cfg = codecs.open("iing.cfg", "r", "utf8").read().split("\n")
    for line in cfg:
        param = line.split(" ")
        if param[0] == "nodename":
            nodename = param[1]
        elif param[0] == "nodedsc":
            nodedsc = " ".join(param[1:])
        elif param[0] == "echo":
            echoareas.append([param[1], " ".join(param[2:])])
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

def get_echoarea(echoarea):
    try:
        blacklist = open("blacklist.txt", "r").read().split("\n")
        result = []
        for msgid in open("echo/" + echoarea, "r").read().split("\n"):
            if msgid != "" and not msgid in blacklist:
                result.append(msgid)
        return result
    except:
        return []

def get_msg(msgid):
    try:
        return codecs.open("msg/" + msgid, "r", "utf8").read()
    except:
        return ""

def get_echoarea_count(echoarea):
    blacklist = open("blacklist.txt", "r").read().split("\n")
    result = 0
    try:
        for msgid in open("echo/" + echoarea, "r").read().split("\n"):
            if msgid != "" and not msgid in blacklist:
                result = result + 1
        return str(result)
    except:
        return "0"

def get_last_msg(echoarea):
    try:
        return codecs.open("msg/" + get_echoarea(echoarea)[-1], "r", "utf8").read().split("\n")
    except:
        return []

def get_last_msgid(echoarea):
    try:
        return get_echoarea(echoarea)[-1]
    except:
        return False

def formatted_time(timestamp):
    return time.strftime("%d.%m.%y %H:%M UTC", time.gmtime(int(timestamp)))

def get_time(echoarea):
    try:
        time = int(open("msg/" + get_echoarea(echoarea)[-1], "r").read().split("\n")[2])
    except:
        time = 0
    return time

def echo_filter(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{1,60}\.[a-z0-9_!.-]{1,60}$')
    if rr.match(ea): return True

def msg_filter(msgid):
    rr = re.compile(r'^[a-z0-9A-Z]{20}$')
    if rr.match(msgid): return True

def create_echoarea(echoarea):
    if not os.path.exists("echo/" + echoarea):
        open("echo/" + echoarea, "w")

def hsh(msg):
    ret = base64.urlsafe_b64encode(hashlib.sha256(msg.encode()).digest()).decode("utf-8").replace("-", "A").replace("_", "z")[:20]
    return ret

def toss_msg(msgfrom, addr, tmsg):
#    try:
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
#    except:
#        msg = None
    if msg:
        if len(msg) <= 65535:
            h = hsh(msg)
            open("echo/" + echoarea, "a").write(h + "\n")
            codecs.open("msg/" + h, "w", "utf8").write(msg)
            return "msg ok:" + h
        else:
            return "msg big!"
    else:
        return "error:unknown"

def body_render(body):
    body = body.strip()
    body = body.replace("<", "&lt;").replace(">", "&gt;")
    rr = re.compile("((^|\n)[a-zA-Zа-яА-Я0-9_-]{0,20}(&gt;){1,20}.+)")
    body = rr.sub(r"<span class='quote'>\1</span>", body)
    rr = re.compile("((^|\n)(PS|P.S|ps|ЗЫ|З.Ы|\/\/|#).*)")
    body = rr.sub(r"\n<span class='comment'>\1</span>", body)
    rr = re.compile("((http|https|ftp):\/\/[a-z_0-9-.]+\\.[a-z]{2,5}(\/[^ \t<>\n\r]+)?\/?)")
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
        if line == "====<br>" and pre == 0:
            pre = 1
            txt += "<pre>====\n"
        elif line == "====<br>" or line == "====" and pre == 1:
            pre = 0
            txt += "====</pre>\n"
        elif pre == 1:
            txt += line.replace("<br>", "") + "\n"
        else:
            txt += line + "\n"
    return txt

def get_file_size(filename):
    return os.stat("files/" + filename).st_size

def get_file_index():
    result = []
    files = codecs.open("files/indexes/files.txt", "r", "utf8").read().split("\n")
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            try:
                size = str(get_file_size(fi[0]))
            except:
                size = "0"
            result.append([fi[0], size, " ".join(fi[1:]) + "\n"])
    return result

def get_public_file_index():
    result = []
    files = codecs.open("files/indexes/public_files.txt", "r", "utf8").read().split("\n")
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            try:
                size = str(get_file_size(fi[0]))
            except:
                size = "0"
            result.append([fi[0], size, " ".join(fi[1:]) + "\n"])
    return result

def get_private_file_index(username):
    result = []
    files = codecs.open("files/indexes/" + username + "_files.txt", "r", "utf8").read().split("\n")
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            try:
                size = str(get_file_size(fi[0]))
            except:
                size = "0"
            result.append([fi[0], size, " ".join(fi[1:]) + "\n"])
    return result

def get_fechoarea(fechoarea):
    result = []
    files = codecs.open("fecho/" + fechoarea + ".txt", "r", "utf8").read().split("\n")
    for f in files:
        if len(f) > 0:
            fi = f.split(":")
            result.append([fi[0], ":".join(fi[1:])])
    return result
