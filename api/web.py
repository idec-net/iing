import api, points, base64, math
from api.bottle import *

def get_page(n):
    return math.ceil(n / 50)

def echoes(subscription):
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

        if new > 0:
            last = echoarea_msglist[-new];
        else:
            last = echoarea_msglist[-1];

        temp.append(new)
        temp.append(last)
        if len(last) > 0:
            temp.append(get_page(api.get_echoarea(echoarea[0]).index(last)))
        else:
            temp.append(get_page(len(api.get_echoarea(echoarea[0]))))
        allechoareas.append(temp)
    return allechoareas

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
    if api.nosubscription:
        subscription = api.echoareas
    else:
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
        last = request.get_cookie(echoarea[0], secret='some-secret-key')
        if not last in api.get_echo_msgids(echoarea[0]):
            last = False
        if not last or len(last) == 0:
            last = api.get_last_msgid(echoarea[0])
        if len(last) > 0:
            page = get_page(api.get_echoarea(echoarea[0]).index(last))
        else:
            page = get_page(len(api.get_echoarea(echoarea[0])))
        echoareas.append({"echoname": echoarea[0], "count": api.get_echoarea_count(echoarea[0]), "dsc": echoarea[1], "msg": api.get_last_msg(echoarea[0]), "last": last, "page": page})
    allechoareas = echoes(subscription)
    auth = request.get_cookie("authstr")
    msgfrom, addr = points.check_point(auth)
    feed = request.get_cookie("feed", secret='some-secret-key')
    if not feed:
        feed = 1
    else:
        feed = int(feed)
    return template("tpl/index.tpl", nodename=api.nodename, dsc=api.nodedsc, echoareas=echoareas, allechoareas=allechoareas, addr=addr, auth=auth, background=api.background, nosubscription=api.nosubscription, feed=feed)

@route("/echolist")
def echolist():
    api.load_config()
    echoareas = []
    s = request.get_cookie("subscription", secret='some-secret-key')
    if not s:
        subscription = []
        for ea in api.echoareas:
            subscription.append(ea[0])
        response.set_cookie("subscription", subscription, path="/", max_age=180*24*60*60, secret='some-secret-key')
        s = subscription
    if api.nosubscription:
        subscription = api.echoareas
    else:
        subscription = []
        for ea in s:
            flag = False
            for e in api.echoareas:
                if ea in e:
                    flag = True
                    subscription.append(e)
            if not flag:
                subscription.append([ea, ""])
    allechoareas = echoes(subscription)
    auth = request.get_cookie("authstr")
    msgfrom, addr = points.check_point(auth)
    feed = request.get_cookie("feed", secret='some-secret-key')
    if not feed:
        feed = 1
    else:
        feed = int(feed)
    return template("tpl/echolist.tpl", nodename=api.nodename, dsc=api.nodedsc, allechoareas=allechoareas, addr=addr, auth=auth, background=api.background, nosubscription=api.nosubscription, feed=feed)

def ffeed(echoarea, msgid, page):
    api.load_config()
    msglist = api.get_echoarea(echoarea)
    result = []
    last = request.get_cookie(echoarea, secret='some-secret-key')
    if not last in api.get_echoarea(echoarea):
        last = False
    if not last or len(last) == 0:
        last = api.get_last_msgid(echoarea)
    if not page:
        if not last:
            page = get_page(len(msglist))
            if page == 0:
                page = 1
        else:
            page = get_page(msglist.index(last))
    page = int(page)
    start = page * 50 - 50
    end = start + 50
    for mid in msglist[start:end]:
        msg = api.get_msg(mid).split("\n")
        if len(msg) > 1:
            result.append([mid, msg])
    ea = [ea for ea in api.echoareas if ea[0] == echoarea]
    if len(ea) != 1:
        ea = [echoarea, ""]
    else:
        ea = ea[0]
    auth = request.get_cookie("authstr")
    if len(msglist) <= end:
        end = api.get_last_msgid(echoarea)
    else:
        end = msglist[end]
    response.set_cookie(echoarea, end, path="/", max_age=180*24*60*60, secret='some-secret-key')
    return template("tpl/feed.tpl", nodename=api.nodename, dsc=api.nodedsc, echoarea=ea, page=page, msgs=result, msgid=msgid, background=api.background, auth=auth)

@route("/<e1>.<e2>")
@route("/<e1>.<e2>/<page>")
@route("/<e1>.<e2>/<page>/<msgid>")
def echoreas(e1, e2, msgid=False, page=False):
    echoarea=e1 + "." + e2
    if not request.get_cookie(echoarea):
        response.set_cookie(echoarea, api.get_last_msgid(echoarea), max_age=180*24*60*60, secret='some-secret-key')
    feed = request.get_cookie("feed", secret='some-secret-key')
    if not feed:
        feed = 1
    else:
        feed = int(feed)
    last = msgid or request.get_cookie(echoarea, secret='some-secret-key')
    if not last in api.get_echoarea(echoarea):
        last = False
    if not last or len(last) == 0:
        last = api.get_last_msgid(echoarea)
    index = api.get_echoarea(echoarea)
    if feed == 0 and len(index) > 0 and index[-1] != last and last in index:
        last = index[index.index(last) + 1]
    if len(index) == 0:
        last = False
    if echoarea != "favicon.ico":
        if last:
            feed = request.get_cookie("feed", secret='some-secret-key')
            if not feed:
                feed = 1
            else:
                feed = int(feed)
            if feed == 0:
                redirect("/" + last)
            else:
                return ffeed(echoarea, last, page)
        else:
            redirect("/new/" + echoarea)

@route("/<msgid>")
def showmsg(msgid):
    api.load_config()
    if api.msg_filter(msgid):
        body = api.get_msg(msgid).split("\n")
        if body != [""]:
            msgfrom, addr = points.check_point(request.get_cookie("authstr"))
            kludges = body[0].split("/")
            if "repto" in kludges:
                repto = kludges[kludges.index("repto") + 1]
            else:
                repto = False
            if len(body) > 0:
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
            auth = request.get_cookie("authstr")
            feed = request.get_cookie("feed", secret='some-secret-key')
            if not feed:
                feed = 1
            else:
                feed = int(feed)
            if feed == 1:
                try:
                    page = get_page(api.get_echoarea(echoarea[0]).index(msgid))
                except:
                    page = get_page(api.get_echoarea_count(echoarea[0]))
            else:
                page = False
            return template("tpl/message.tpl", nodename=api.nodename, echoarea=echoarea, index=index, msgid=msgid, repto=repto, current=current, time=t, point=point, address=address, to=to, subj=subj, body=body, msgfrom=msgfrom, background=api.background, auth=auth, feed=feed, page=page)
        else:
            redirect("/")
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
        if not msgid:
            page = get_page(len(msglist))
        else:
            page = get_page(msglist.index(msgid))
        if page == 0:
            page = 1
    return template("tpl/msglist.tpl", nodename=api.nodename, dsc=api.nodedsc, page=int(page), echoarea=ea, msgid=msgid, msglist=result, topiclist=False, background=api.background)

@route("/new/<e1>.<e2>")
@route("/reply/<e1>.<e2>")
@route("/reply/<e1>.<e2>/<msgid>")
def reply(e1, e2, msgid = False):
    echoarea = e1 + "." + e2
    auth = request.get_cookie("authstr")
    if msgid:
        msg = api.get_msg(msgid).split("\n")
    else:
        msg = False
    return template("tpl/reply.tpl", nodename=api.nodename, dsc=api.nodedsc, echoarea=echoarea, msgid=msgid, msg=msg, auth=auth, hidehome=False, topiclist=False, background=api.background)

@post("/a/savemsg/<echoarea>")
@post("/a/savemsg/<echoarea>/<msgid>")
def save_messsage(echoarea, msgid = False):
    if api.echo_filter(echoarea):
        subj = request.forms.get("subj")
        msgbody = request.forms.get("msgbody")
        if len(subj) > 0 and len(msgbody) > 0:
            pauth = request.forms.get("authstr")
            msgfrom, addr = points.check_point(pauth)
            if not addr:
                return "auth error!"
            response.set_cookie("authstr", pauth, path="/", max_age=3600000000)
            msg = ""
            msg = msg + echoarea + "\n"
            msg = msg + request.forms.get("to") + "\n"
            msg = msg + subj + "\n\n"
            if msgid:
                msg = msg + "@repto:" + msgid + "\n"
            msg = msg + msgbody
            msg = base64.b64encode(msg.encode("utf8"))
            message=api.toss_msg(msgfrom, addr, msg)
            if message.startswith("msg ok"):
                redirect("/%s" % message[7:])
        else:
            redirect("/")

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

@route("/s/download/<filename:path>")
def download(filename):
    filename = filename.split("/")
    return static_file(filename[-1], "files/%s" % "/".join(filename[:-1]))

@route("/s/blacklisted/<msgid>")
def blacklist(msgid):
    if api.msg_filter(msgid):
        auth = request.get_cookie("authstr")
        if points.is_operator(auth):
            api.delete_msg(msgid)
            open("blacklist.txt", "a").write(msgid + "\n")
    redirect("/")

@route("/s/feed/<feed>")
def sfeed(feed):
    response.set_cookie("feed", feed, path="/", max_age=3600000000, secret='some-secret-key')
    redirect("/profile")

@route("/login")
@post("/login")
def login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    auth = points.login(username, password)
    if auth:
        if auth != "error":
            response.set_cookie("authstr", auth, path="/", max_age=3600000000)
            redirect("/")
        else:
            return template("tpl/login.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, username=username, auth=auth, registration=api.registration, alarm="Неверные учётные данные!")
    return template("tpl/login.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, registration=api.registration, username=False, auth=False, alarm=False)

@route("/profile")
def profile():
    auth = request.get_cookie("authstr")
    username, addr = points.check_point(auth)
    feed = request.get_cookie("feed", secret='some-secret-key')
    if not feed:
        feed = 1
    else:
        feed = int(feed)
    return template("tpl/profile.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, username=username, auth=auth, addr=addr, feed=feed)

@route("/logout")
def logout():
    response.set_cookie("authstr", "", path="/", max_age=-1, expires=0)
    redirect("/")

@route("/registration")
@post("/registration")
def registration():
    if api.registration:
        username = request.forms.get("username")
        password = request.forms.get("password")
        if username and password:
            if points.check_username(username):
                return template("tpl/registration.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, alarm="Имя пользователя уже существует.")
            else:
                hsh, phash = points.make_point(username, password)
                points.save_point(phash, username, hsh)
                response.set_cookie("authstr", phash, path="/", max_age=3600000000)
                redirect("/")
        return template("tpl/registration.tpl", nodename=api.nodename, dsc=api.nodedsc, background=api.background, alarm=False)
    else:
        redirect("/")

@route("/rss/<echoarea>")
def rss(echoarea):
    response.set_header("content-type", "application/rss+xml; charset=utf-8")
    api.load_config()
    msglist = api.get_echoarea(echoarea)
    msgs = []
    for msgid in msglist[-50:]:
        msgs.append([msgid, api.get_msg(msgid).split("\n")])
    return template("tpl/rss.tpl", nodename=api.nodename, dsc=api.nodedsc, nodeurl=api.nodeurl, msgs=reversed(msgs), echoarea=echoarea)

@route("/lib/css/<filename>")
def pcss(filename):
    return static_file(filename, root="lib/css/")

@route("/lib/fonts/<filename>")
def pcss(filename):
    return static_file(filename, root="lib/fonts/")

@route("/lib/<filename>")
def plib(filename):
    return static_file(filename, root="lib/")
