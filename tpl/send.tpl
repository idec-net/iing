%include tpl/header.tpl nodename=nodename, dsc=dsc, hidemenu=True, background=background
<br>
<div id="content" class="single-message">
<b>{{message}}</b>
%if message.startswith("msg ok:"):
%msgid = message[7:]
<br><a href="/{{msgid}}">Перейти к сообщению</a>
<br><a href="/{{echoarea}}">Перейти к конференции</a>
<br><a href="/">На главную</a>
</div>
%include tpl/footer.tpl