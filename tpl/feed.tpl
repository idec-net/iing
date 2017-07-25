%import api, re, points, math
%include tpl/header.tpl nodename=nodename, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
<a href="/echolist" id="echolist-button" class="button"><i class="fa fa-bars"></i></a>
</div>
<h3><span class="caption"><i class="fa fa-comments"></i> {{echoarea[0]}}: {{echoarea[1]}}</span></h3>
<div id="rbuttons">
<a href="/new/{{echoarea[0]}}" class="button"><i class="fa fa-plus-circle"></i><span class="caption"> Новое</span></a>
</div>
</div>
<br>
%include tpl/fpaginator.tpl echoarea=echoarea[0], msglist=msgs, page=page, onpage=50
%start = (page - 1) * 50
%if start + 50 > len(msgs):
%last = len(msgs)
%else:
%last = start + 50
%end

<table cellpadding="0" cellsspacing="0" id="content">
<tr>
<td>
%for msg in msgs:
<a name="{{msg[0]}}"></a>
%if msg[0] == msgid:
<div class="single-message current-message">
%else:
<div class="single-message">
%end
<div id="echo-buttons">
<a href="/{{msg[0]}}" class="echo-button" title="Ссылка на сообщение"><i class="fa fa-eye"></i></a>
<a href="/reply/{{echoarea[0]}}/{{msg[0]}}" class="echo-button" title="Ответить"><i class="fa fa-reply"></i></a>
</div>
%if points.is_operator(auth):
<a class="blacklisted" href="/s/blacklisted/{{msg[0]}}" title="Поместить сообщение в ЧС"><i class="fa fa-trash"></i></a>
%end

%kludges = msgs[1][0].split("/")
%if "repto" in kludges:
%repto = kludges[kludges.index("repto") + 1]
%else:
%repto = False
%end
%t = api.formatted_time(msg[1][2])
%point = msg[1][3]
%address = msg[1][4]
%to = msg[1][5]
%subj = msg[1][6]
%body = msg[1][8:]

<div class="message-header">
%if repto:
<b>Ответ на:</b> <a href="/{{repto}}">{{repto}}</a><br>
%end
<b>От:</b> {{point}} ({{address}}) {{t}}<br>
<b>Кому:</b> {{to}}<br>
<b>Тема:</b> {{subj}}
</div>
{{!api.body_render("\n".join(body))}}
</div><br>
%end
</table>
%include tpl/fpaginator.tpl echoarea=echoarea[0], msglist=msgs, page=page, onpage=50
<br>
%include tpl/footer.tpl