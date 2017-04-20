import api, points, base64, math
from api.bottle import *

@route("/")
def index():
    api.load_config()
    echoareas = []
    s = request.get_cookie("subscription", secret='some-secret-key')
    if not s:
        subscription = []
        for ea in api.echoareas:
            subscription.append(ea[0])
        response.set_cookie("subscription", subscription, path="/", max_age=180*24*60*60, secret='some-secret-key')
        s = subscription
    subscription = []
    for ea in s:
        flag = False
        for e in api.echoareas:
            if ea in e:
                flag = True
                subscription.append(e)
        if not flag:
            subscription.append([ea, ""])
    ea = [[echoarea[0], echoarea[1], api.get_time(echoarea[0])] for echoarea in subscription]
    for echoarea in sorted(ea, key=lambda ea: ea[2], reverse=True)[0:5]:
        echoareas.append({"echoname": echoarea[0], "count": api.get_echoarea_count(echoarea[0]), "dsc": echoarea[1], "msg": api.get_last_msg(echoarea[0])})
    allechoareas = []
    for echoarea in subscription:
        temp = echoarea
        if not request.get_cookie(echoarea[0]):
            response.set_cookie(echoarea[0], api.get_last_msgid(echoarea[0]), path="/", max_age=180*24*60*60, secret='some-secret-key')
        current = request.get_cookie(echoarea[0], secret='some-secret-key')
        if not current:
            current = api.get_last_msgid(echoarea[0])
        echoarea_msglist = api.get_echoarea(echoarea[0])
        if len(echoarea_msglist) > 0 and current in echoarea_msglist:
            new = int(api.get_echoarea_count(echoarea[0])) - echoarea_msglist.index(current) - 1
        else:
            new = 0
        temp.append(new)
        allechoareas.append(temp)
    auth = request.get_cookie("authstr")
    msgfrom, addr = points.check_point(auth)
    return template("tpl/index.tpl", nodename=api.nodename, dsc=api.nodedsc, echoareas=echoareas, allechoareas=allechoareas, addr=addr, auth=auth, background=api.background)

@route("/<e1>.<e2>")
def echoreas(e1, e2):
    echoarea=e1 + "." + e2
    if not request.get_cookie(echoarea):
        response.set_cookie(echoarea, api.get_last_msgid(echoarea), max_age=180*24*60*60, secret='some-secret-key')
    last = request.get_cookie(echoarea, secret='some-secret-key')
    if not last:
        last = api.get_last_msgid(echoarea)
    index = api.get_echoarea(echoarea)
    if len(index) > 0 and index[-1] != last and last in index:
        last = index[index.index(last) + 1]
    else:
        last = api.get_last_msgid(echoarea)
    if len(index) == 0:
        last = False
    if echoarea != "favicon.ico":
        if last:
            redirect("/" + last)
        else:
            redirect("/new/" + echoarea)

@route("/<msgid>")
def showmsg(msgid):
    api.load_config()
    if api.msg_filter(msgid):
        body = api.get_msg(msgid).split("\n")
        if len(body) > 0:
            msgfrom, addr = points.check_point(request.get_cookie("authstr"))
            kludges = body[0].split("/")
            if "repto" in kludges:
                repto = kludges[kludges.index("repto") + 1]
            else:
                repto = False
            if body:
                echoarea = [ea for ea in api.echoareas if ea[0] == body[1]]
                if len(echoarea) == 0:
                    echoarea = [body[1], ""]
                else:
                    echoarea = echoarea[0]
            else:
                echoarea = ["", ""]
            t = api.formatted_time(body[2])
            point = body[3]
            address = body[4]
            to = body[5]
            subj = body[6]
            body = body[8:]
            index = api.get_echoarea(echoarea[0])
            current = index.index(msgid)
            response.set_cookie(echoarea[0], msgid, max_age=180*24*60*60, secret='some-secret-key')
            return template("tpl/message.tpl", nodename=api.nodename, echoarea=echoarea, index=index, msgid=msgid, repto=repto, current=current, time=t, point=point, address=address, to=to, subj=subj, body=body, msgfrom=msgfrom, background=api.background)
        else:
            redirect("/")
    else:
        redirect("/")

@route("/<msgid>/m")
@route("/<msgid>/m/<page:int>")
def showmsg(msgid, page=0):
    if api.msg_filter(msgid):
        return template("tpl/message.tpl", nodename=api.nodename, dsc=api.nodedsc, page=page, msgid=msgid, hidehome=False, topiclist=False, shortlist=True, background=api.background)
    else:
        redirect("/")

@route("/msglist/<echoarea>")
@route("/msglist/<echoarea>/<msgid>")
@route("/msglist/<echoarea>/<msgid>/<page>")
def msg_list(echoarea, page=False, msgid=False):
    api.load_config()
    msglist = api.get_echoarea(echoarea)
    result = []
    for mid in msglist:
        msg = api.get_msg(mid).split("\n")
        try:
            subject = msg[6]
            f = msg[3]
            t = msg[5]
            result.append({"msgid": mid, "subject": subject, "from": f, "to": t})
        except:
            None
    ea = [ea for ea in api.echoareas if ea[0] == echoarea][0]
    if not page:
        page = math.ceil(msglist.index(msgid) / 50)
        if page == 0:
            page = 1
    return template("tpl/msglist.tpl", nodename=api.nodename, dsc=api.nodedsc, page=int(page), echoarea=ea, msgid=msgid, msglist=result, topiclist=False, background=api.background)

@route("/new/<e1>.<e2>")
@route("/reply/<e1>.<e2>")
@route("/reply/<e1>.<e2>/<msgid>")
def reply(e1, e2, msgid = False):
    echoarea = e1 + "." + e2
    auth = request.get_cookie("authstr")
    return template("tpl/reply.tpl", nodename=api.nodename, dsc=api.nodedsc, echoarea=echoarea, msgid=msgid, auth=auth, hidehome=False, topiclist=False, background=api.background)

@post("/a/savemsg/<echoarea>")
@post("/a/savemsg/<echoarea>/<msgid>")
def save_messsage(echoarea, msgid = False):
    if api.echo_filter(echoarea):
        pauth = request.forms.get("authstr")
        msgfrom, addr = points.check_point(pauth)
        if not addr:
            return "auth error!"
        response.set_cookie("authstr", pauth, path="/", max_age=3600000000)
        msg = ""
        msg = msg + echoarea + "\n"
        msg = msg + request.forms.get("to") + "\n"
        msg = msg + request.forms.get("subj") + "\n\n"
        if msgid:
            msg = msg + "@repto:" + msgid + "\n"
        msg = msg + request.forms.get("msgbody")
        msg = base64.b64encode(msg.encode("utf8"))
        return template("tpl/send.tpl", nodename=api.nodename, dsc=api.nodedsc, message=api.toss_msg(msgfrom, addr, msg), echoarea=echoarea, background=api.background)

@post("/s/subscription")
@route("/s/subscription")
def subscription():
    api.load_config()
    s = request.forms.get("subscription")
    subscription = []
    if request.forms.get("default"):
        for ea in api.echoareas:
            subscription.append(ea[0])
        response.set_cookie("subscription", subscription, path="/", max_age=180*24*60*60, secret='some-secret-key')
        redirect("/")
    if s:
        for ea in s.strip().replace("\r", "").split("\n"):
            if api.echo_filter(ea):
                subscription.append(ea)
        response.set_cookie("subscription", subscription, path="/", max_age=180*24*60*60, secret='some-secret-key')
        redirect("/")
    subscription = request.get_cookie("subscription", secret='some-secret-key')
    echoareas = []
    for echoarea in api.echoareas:
        echoareas.append([echoarea[0], api.get_echoarea_count(echoarea[0]), echoarea[1]])
    return template("tpl/subscription.tpl", nodename=api.nodename, dsc=api.nodedsc, echoareas=echoareas, subscription=subscription, background=api.background)

@route("/s/filelist")
def filelist():
    auth = request.get_cookie("authstr")
    msgfrom, addr = points.check_point(auth)
    files = api.get_public_file_index()
    if not addr:
        return template("tpl/filelist.tpl", nodename=api.nodename, dsc=api.nodedsc, files=sorted(files), auth=False, background=api.background)
    files = files + api.get_file_index()
    try:
        files = files + api.get_private_file_index(msgfrom)
    except:
        None
    return template("tpl/filelist.tpl", nodename=api.nodename, dsc=api.nodedsc, files=sorted(files), auth=auth, background=api.background)

@route("/login")
@post("/login")
def login():
    username = request.forms.get("username")
    auth = request.forms.get("authstr")
    msgfrom, addr = points.check_point(auth)
    if addr:
        if msgfrom == username:
            response.set_cookie("authstr", auth, path="/", max_age=3600000000)
            redirect("/")
        else:
            return template("tpl/login.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, username=username, auth=auth, alarm="Неверные учётные данные!")
    return template("tpl/login.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, username=False, auth=False, alarm=False)

@route("/logout")
def logout():
    response.set_cookie("authstr", "", path="/", max_age=-1, expires=0)
    redirect("/")

@route("/lib/css/<filename>")
def pcss(filename):
    return static_file(filename, root="lib/css/")

@route("/lib/fonts/<filename>")
def pcss(filename):
    return static_file(filename, root="lib/fonts/")

@route("/lib/<filename>")
def plib(filename):
    return static_file(filename, root="lib/")
