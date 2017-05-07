%import api
%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<h3><img src="/lib/idec_grey.png" width="20"><span class="caption"> {{dsc}}</span></h3>
<a href="/echolist" id="echolist-button" class="button"><i class="fa fa-bars"></i></a>
<div id="rbuttons">
<a href="http://ii-net.tk/" class="button"><i class="fa fa-info-circle"></i><span class="caption"> О нас</span></a>
<a href="/s/subscription" class="button"><i class="fa fa-paper-plane"></i><span class="caption"> Подписки</span></a>
<a href="/s/filelist" class="button"><i class="fa fa-floppy-o"></i><span class="caption"> Файлы</span></a>
%if addr:
<a href="/logout" class="button"><i class="fa fa-sign-out"></i><span class="caption"> Выйти</span></a>
%else:
<a href="/login" class="button"><i class="fa fa-sign-in"></i><span class="caption"> Войти</span></a>
%end
</div>
</div>

<table id="content" cellpadding="0" cellspacing="0">
<tr>
<td id="side-menu">
<div id="conferences">
<center><b>Список конференций</b></center>
%for echoarea in allechoareas:
%if echoarea[2] == 0:
<a href="/{{echoarea[0]}}" class="new-button-link echo-button-link" title="{{echoarea[1]}}"><i class="fa fa-comments"></i>
 {{echoarea[0]}}<span class="unread">0</span></a>
%else:
<a href="/{{echoarea[0]}}" class="new-button-link" title="{{echoarea[1]}}"><i class="fa fa-comments"></i> {{echoarea[0]}}<span class="unread">{{echoarea[2]}}</span></a>
%end
%end
</div>
</td>
<td>

%for echoarea in echoareas:
%last_msgid = api.get_last_msgid(echoarea["echoname"])
%if last_msgid:
<h2 class="echo-title"><a href="/{{echoarea["echoname"]}}">{{echoarea["echoname"]}}</a> <i class="fa fa-envelope-o"></i> {{echoarea["count"]}}</h2>
%else:
<a class="echoarea-link" href="/{{echoarea["echoname"]}}"><h2 class="echo-title">{{echoarea["echoname"]}}</a> <i class="fa fa-envelope-o"></i> {{echoarea["count"]}}</h2>
%end
%if len(echoarea["msg"]) > 0:
<div class="message">
%#<h3 class="message-title">{{echoarea["msg"][6]}}</h3>
<b title="{{echoarea["msg"][4]}}">{{echoarea["msg"][3]}}</b> to {{echoarea["msg"][5]}} @ {{echoarea["msg"][6]}} <i class="fa fa-clock-o"></i>  {{api.formatted_time(echoarea["msg"][2])}}<br><br>
%if len(echoarea["msg"][8:]) <= 10:
%body = api.body_render("\n".join(echoarea["msg"][8:]))
%else:
%body = api.body_render("\n".join(echoarea["msg"][8:12])) + "<br><br><a href=" + last_msgid + ">Читать далее</a>"
%end
{{!body}}
</div>
%end
%end
</td>
</tr>
</table>
<br>
%include tpl/footer.tpl