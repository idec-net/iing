%import api, math
%include tpl/header.tpl nodename=nodename, dsc=dsc, echoarea=False, hidehome=False, hidemenu=False, background=background

<div id="bottom-buttons">
<a href="/" title="Главная"><i class="fa fa-home fa-2x bbutton"></i></a>
<i class="fa fa-arrow-circle-up fa-2x bbutton" onclick="document.body.scrollTop = document.documentElement.scrollTop = 0;" title="Наверх"></i>
</div>

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
<h3><span class="caption">{{echoarea[0]}}: {{echoarea[1]}}</span></h3>
%if msgid:
<div id="rbuttons">
<a href="/{{msgid}}" class="button"><i class="fa fa-arrow-circle-left"></i><span class="caption"> Назад</span></a>
</div>
%end
</div><br>

%if not page:
%page = math.ceil(len(msglist) / 50)
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