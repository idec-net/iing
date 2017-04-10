%import api, math
%include tpl/header.tpl nodename=nodename, dsc=dsc, echoarea=False, hidehome=False, hidemenu=False, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i> Главная</a>
</div>
<h3>{{echoarea[0]}}: {{echoarea[1]}}</h3>
%if msgid:
<div id="rbuttons">
<a href="/{{msgid}}" class="button"><i class="fa fa-arrow-circle-left"></i> Назад</a>
</div>
%end
</div><br>

%if not page:
%page = len(msglist) / 50
%if page - math.floor(page) > 0:
%page = math.floor(page) + 1
%else:
%page = math.floor(page)
%end
%end
%include tpl/paginator.tpl echoarea=echoarea[0], msglist=msglist, page=page, onpage=50, shortlist=True
%start = (page - 1) * 50
%if start + 50 > len(msglist):
%last = len(msglist)
%else:
%last = start + 50
%end

<div id="content">
<table cellpaddint="0" cellspacing="0" class="single-message msglist">
<tr>
<th>Тема</th>
<th align="right">От кого &#x279C; Кому</th>
</tr>
%for msg in msglist[start:last]:
%if msg["msgid"] == msgid:
<tr class="current-echorow">
<td><a name="{{msg["msgid"]}}"></a><a href="/{{msg["msgid"]}}">{{msg["subject"]}}</a></td>
<td style="text-align: right;">{{msg["from"]}} &#x279C; {{msg["to"]}}</td>
</tr>
%else:
<tr class="echorow">
<td><a name="{{msg["msgid"]}}"></a><a href="/{{msg["msgid"]}}">{{msg["subject"]}}</a></td>
<td style="text-align: right;">{{msg["from"]}} &#x279C; {{msg["to"]}}</td>
</tr>
%end
%end
</table>
</div>
%include tpl/paginator.tpl echoarea=echoarea[0], msglist=msglist, page=page, onpage=50, shortlist=True
<br>
%include tpl/footer.tpl