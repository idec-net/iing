%include tpl/header.tpl nodename=nodename, dsc=dsc, hidemenu=True, background=background
%if msgid:
%title="Ответ на " + msgid
%msg = open("msg/" + msgid, "r").read().split("\n")
%repto = msgid
%to = msg[3]
%subj = msg[6]
%if not subj.startswith("Re: "):
%subj = "Re: " + subj
%end
%else:
%title="Новое сообщение в " + echoarea
%repto = ""
%to = "All"
%subj = False
%end
<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i> Главная</a>
</div>
<h3>{{title}}</h3>
</div>
<br>
<div id="conferences" class="width90">
%if msgid:
<div id="content" class="single-message reply">
%for line in msg[8:]:
{{line}}<br>
%end
</div><br>
%end

<br>
<center>
%if msgid:
<form method="post" enctype="multipart/form-data" action="/a/savemsg/{{echoarea}}/{{msgid}}">
%else:
<form method="post" enctype="multipart/form-data" action="/a/savemsg/{{echoarea}}">
%end
<input type="hidden" name="repto" value="{{repto}}">
<input type="hidden" name="to" value="{{to}}">
%if subj:
<input type="text" name="subj" class="input input_line" placeholder="Тема сообщения" value="{{subj}}"><br>
%else:
<input type="text" name="subj" class="input input_line" placeholder="Тема сообщения"><br>
%end
<textarea name="msgbody" cols="80" rows=10" class="input" placeholder="Введите текст сообщения..."></textarea><br>
%if not auth:
<input type="text" name="authstr" class="input input_line" placeholder="auth-ключ"><br>
%else:
<input type="hidden" name="authstr" class="input input_line" placeholder="auth-str" value={{auth}}><br>
%end
<button class="form-button"><i class="fa fa-share-square"></i> Отправить</button>
</form>
</center>
</div>
<br>
%include tpl/footer.tpl