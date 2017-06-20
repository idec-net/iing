#!/usr/bin/env python3

import api, points, base64, time, codecs, os, hashlib
from api.bottle import *
from shutil import copyfile

def write_to_log(line):
    ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    timestump = time.strftime("%d.%m.%y %H:%M", time.gmtime(int(time.time())))
    open("iing.log", "a").write("%s, %s: %s\n" %(timestump, ip, line))

@route("/list.txt")
def list_txt():
    write_to_log("list.txt")
    response.set_header("content-type", "text/plain; charset=utf-8")
    echoareas = api.echoareas
    echoareas = echoareas + api.shortareas
    echolist = ""
    for echoarea in sorted(echoareas, key=lambda echoareas: echoareas[0]):
        try:
            echolist = echolist + "%s:%s:%s\n" % (echoarea[0], api.get_echoarea_count(echoarea[0]), echoarea[1])
        except:
            echolist = echolist + "%s:0:%s\n" % (echoarea[0], echoarea[1])
    return echolist

@route("/u/e/<names:path>")
def index_list(names):
    write_to_log("u/e/%s" % names)
    response.set_header('content-type','text/plain; charset=utf-8')
    result = ""
    r = False
    s = 0
    e = 0
    names = names.split("/")
    if ":" in names[-1]:
        s = int(names[-1].split(":")[0])
        e = int(names[-1].split(":")[1])
        r = True
        names = names[0:-1]
    for echoarea in names:
        result = result + echoarea + "\n"
        try:
            ss = s
            if s < 0 and s + int(api.get_echoarea_count(echoarea)) < 0:
                ss = 0
            elif s > int(api.get_echoarea_count(echoarea)):
                ss = e * -1
            if r:
                if s + e == 0:
                    msglist = api.get_echoarea(echoarea)[ss:]
                else:
                    msglist = api.get_echoarea(echoarea)[ss:ss + e]
            else:
                msglist = api.get_echoarea(echoarea)
            result = result + "\n".join(msglist) + "\n"
        except: result = result + ""
    return result

@route("/u/m/<msgids:path>")
def outmsg(msgids):
    response.set_header ('content-type','text/plain; charset=utf-8')
    result = ""
    for msgid in msgids.split("/"):
        result = result + msgid + ":"
        try:
            msg = str.encode(codecs.open("msg/" + msgid, "r", "utf8").read())
            result = result + (base64.b64encode(msg)).decode("utf-8") + "\n"
        except:
            result = result + "\n"
    return result

def point(pauth, tmsg):
    msgfrom, addr = points.check_point(pauth)
    if not addr:
        return "auth error!"
    return api.toss_msg(msgfrom, addr, tmsg)

@route("/u/point/<pauth>/<tmsg:path>")
def point_get(pauth, tmsg):
    write_to_log("point/%s GET\n" % pauth)
    return point(pauth, tmsg)

@post("/u/point")
def point_post():
    write_to_log("point/%s POST" % request.POST["pauth"])
    return point(request.POST["pauth"], request.POST["tmsg"])

@route("/blacklist.txt")
def blacklist_txt():
    write_to_log("blacklist.txt")
    response.set_header("content-type", "text/plain; charset=utf-8")
    return open("blacklist.txt", "r").read()

@route("/e/<echoarea>")
def e(echoarea):
    write_to_log("e/%s" % echoarea)
    response.set_header("content-type", "text/plain; charset=utf-8")
    return "\n".join(api.get_echoarea(echoarea))

@route("/m/<msgid>")
def m(msgid):
    response.set_header("content-type", "text/plain; charset=utf-8")
    try:
        return codecs.open("msg/" + msgid, "r", "utf8").read()
    except:
        return ""

@route("/x/small-echolist")
def x_small_echolist():
    write_to_log("x/small-echolist")
    response.set_header("content-type", "text/plain; charset=utf-8")
    api.load_config()
    echoareas = api.echoareas
    echoareas = echoareas + api.shortareas
    echolist = ""
    for echoarea in sorted(echoareas, key=lambda echoareas: echoareas[0]):
        echolist = echolist + echoarea[0] + "\n"
    return echolist

@route("/x/caesium")
def x_caesium():
    write_to_log("x/caesium")
    response.set_header("content-type", "text/plain; charset=utf-8")
    api.load_config()
    echoareas = api.echoareas
    echoareas = echoareas +api.shortareas
    echolist = ""
    for echoarea in sorted(echoareas, key=lambda echoareas: echoareas[0]):
        echolist = echolist + "echo %s %s\n" % (echoarea[0], echoarea[1])
    return echolist

@route("/x/file")
def file_error():
    response.set_header("content-type", "text/plain; charset=utf-8")
    return get_public_file_index()

@route("/x/filelist")
def public_filelist():
    write_to_log("x/filelist")
    response.set_header("content-type", "text/plain; charset=utf-8")
    result = ""
    for f in sorted(api.get_public_file_index(), key = lambda x: x[0]):
        result = result + ":".join(f)
    return result

@post("/x/filelist")
@route("/x/filelist/<pauth>")
def private_filelist(pauth = False):
    response.set_header("content-type", "text/plain; charset=utf-8")
    if not pauth:
        try:
            pauth = request.POST["pauth"]
        except:
            return "auth error!"
    write_to_log("x/filelist %s" % pauth)
    result = ""
    files = sorted(api.get_public_file_index())
    msgfrom, addr = points.check_point(pauth)
    if not addr:
        for f in sorted(files):
            result = result + ":".join(f)
        return result
    files = files + api.get_file_index()
    try:
        files = files + api.get_private_file_index(msgfrom)
    except:
        None
    for f in sorted(files):
        result = result + ":".join(f)
    return result

@route("/x/file/<filename:path>")
def get_public_file(filename):
    ip = request['REMOTE_ADDR']
    open("iing.log", "a").write("%s: x/file/%s\n" % (ip, filename))
    response.set_header("content-type", "text/plain; charset=utf-8")
    public_files = []
    for line in codecs.open("files/indexes/public_files.txt", "r", "utf8").read().split("\n"):
        try:
            public_files.append(line.split(":")[0])
        except:
            None
    if filename in public_files:
        return static_file(filename, "files/")
    else:
        return "file not found"

@post("/x/file")
def post_file():
    response.set_header("content-type", "text/plain; charset=utf-8")
    try:
        pauth = request.POST["pauth"]
    except:
        pauth = False
    try:
        filename = request.POST["filename"]
    except:
        filename = False
    if not filename:
        return "not filename found"
    write_to_log("x/file/%s/%s POST" % (pauth, filename))
    files = []
    msgfrom, addr = points.check_point(pauth)
    if addr:
        for line in codecs.open("files/indexes/public_files.txt", "r", "utf8").read().split("\n"):
            try:
                files.append(line.split(":")[0])
            except:
                None
        for line in codecs.open("files/indexes/files.txt", "r", "utf8").read().split("\n"):
            try:
                files.append(line.split(":")[0])
            except:
                None
        if os.path.exists("files/indexes/" + msgfrom + "_files.txt"):
            for line in codecs.open("files/indexes/" + msgfrom + "_files.txt", "r", "utf8").read().split("\n"):
                try:
                    files.append(line.split(":")[0])
                except:
                    None
        fechoes = []
        for fecho in os.listdir("fecho"):
            fechoes.append(fecho)
        for fecho in fechoes:
            f = codecs.open("fecho/%s" % fecho, "r").read().split("\n")
            for row in f:
                if len(row) > 0:
                    r = row.split(":")
                    files.append(fecho + "/" + r[1])
        if filename in files:
            return static_file(filename, "files/")
        else:
            return "file not found"
    files = []
    for line in codecs.open("files/indexes/public_files.txt", "r", "utf8").read().split("\n"):
        try:
            files.append(line.split(":")[0])
        except:
            None
    if filename in files:
        return static_file(filename, "files/")
    else:
        return "file not found"

@route("/x/c/<echoareas:path>")
def xc(echoareas):
    write_to_log("x/c/%s" % echoareas)
    response.set_header("content-type", "text/plain; charset=utf-8")
    try:
        echoareas = echoareas.split("/")
        ret = []
        for echoarea in echoareas:
            ret.append("%s:%s" %(echoarea, api.get_echoarea_count(echoarea)))
        return "\n".join(ret)
    except:
        return ""

@route("/x/features")
def features():
    response.set_header("content-type", "text/plain; charset=utf-8")
    return "u/e\nlist.txt\nblacklist.txt\nx/file\nx/small-echolist\nx/caesium\nx/c"

@route("/robots.txt")
def robots():
    response.set_header("content-type", "text/plain; charset=utf-8")
    if api.norobots:
        return "User-agent: *\nDisallow: /"
    else:
        return "User-agent: *\nAllow: /"

@route("/f/c/<fechoes:path>")
def fecho_counts(fechoes):
    response.set_header("content-type", "text/plain; charset=utf-8")
    fechoes = fechoes.split("/")
    counts = ""
    for fecho in fechoes:
        counts = counts + fecho + ":" + str(len(api.get_fechoarea(fecho))) + "\n"
    return counts

@route("/f/e/<fechoes:path>")
def fecho_index(fechoes):
    index = ""
    fechoes = fechoes.split("/")
    ip = request['REMOTE_ADDR']
    open("iing.log", "a").write("%s: f/e/%s\n" % (ip, fechoes))
    response.set_header("content-type", "text/plain; charset=utf-8")
    s = 0
    e = 0
    if ":" in fechoes[-1]:
        s = int(fechoes[-1].split(":")[0])
        e = int(fechoes[-1].split(":")[1])
        r = True
        fechoes = fechoes[0:-1]
    files = []
    if s != 0 and e != 0:
        s = int(s)
        e = int(e)
        for fecho in fechoes:
            ss = s
            if s < 0 and s + len(api.get_fechoarea(fecho)) < 0:
                ss = 0
            elif s > len(api.get_fechoarea(fecho)):
                ss = e * -1
            if s + e == 0:
                for f in api.get_fechoarea(fecho)[ss:]:
                    files.append(f)
            else:
                for f in api.get_fechoarea(fecho)[ss:ss + e]:
                    files.append(f)
    else:
        for fecho in fechoes:
            for f in api.get_fechoarea(fecho):
                files.append(f)
    for row in files:
        index = index + ":".join(row) + "\n"
    return index

@route("/f/f/<fecho>/<fid>")
def fecho_file(fecho, fid):
    if not os.path.exists("fecho/%s" % fecho):
        return "file echo not found"
    fecho_ = open("fecho/%s" % fecho, "r").read().split("\n")
    fids = [f.split(":")[0] for f in fecho_]
    files = [f.split(":")[1] for f in fecho_ if len(f) > 0]
    if not fid in fids:
        return "file not found"
    return static_file(files[fids.index(fid)], "files/%s/" % fecho)

@post("/f/p")
def fecho_post():
    response.set_header("content-type", "text/plain; charset=utf-8")
    try:
        pauth = request.POST["pauth"]
    except:
        pauth = False
    try:
        fecho = request.POST["fecho"]
    except:
        fecho = False
    try:
        f = request.files.get("file")
    except:
        f = False
    try:
        dsc = request.POST["dsc"]
    except:
        dsc = False
    if pauth and fecho and f and dsc:
        if api.fecho_filter(fecho):
            msgfrom, addr = points.check_point(pauth)
            if addr:
                f.save("temp")
                if not os.path.exists("files/%s" % fecho):
                    os.makedirs("files/%s" % fecho)
                hsh = api.fhsh(open("./temp", "rb").read())
                hshs = []
                try:
                    for row in open("fecho/%s" % fecho, "r").read().split("\n"):
                        hshs.append(row.split(":")[0])
                except:
                    None
                if not hsh in hshs:
                    name = f.raw_filename
                    while os.path.exists("files/%s/%s" % (fecho, name)):
                        tmp = name.split(".")
                        name = ".".join(tmp[:-1])
                        suffix = name.split("_")[-1]
                        if suffix == name:
                            suffix = "0"
                        try:
                            s = int(suffix)
                            s += 1
                            post = "_" + str(s)
                        except:
                            post = "_1"
                        if suffix != "0":
                            Name = name.replace("_" + suffix, post) + "." + tmp[-1]
                        else:
                            name = name + post + "." + tmp[-1]
                    try:
                        size = str(os.stat("temp").st_size)
                    except:
                        size = "0"
                    copyfile("temp", "files/%s/%s" % (fecho, name))
                    codecs.open("fecho/%s" % fecho, "a", "utf8").write("%s:%s:%s:%s,%s:%s\n" % (hsh, name, size, api.nodename, addr, dsc.replace("\n", " ")))
                    codecs.open("files/indexes/files.txt", "a", "utf8").write("%s:%s\n" % (name, dsc.replace("\n", " ")))
                else:
                    os.remove("./temp")
                    return "file exists"
                os.remove("./temp")
            else:
                return "auth error!"
        else:
            return "incorrect fileechoarea"

api.init()
api.load_config()

if api.web_interface:
    from api.web import *

run(host="0.0.0.0", port=3000)#, quiet=True)
