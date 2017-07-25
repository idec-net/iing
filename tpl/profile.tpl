%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
<h3>Профиль</h3>
</div><br>

<div id="conferences" class="width90">
<div align="left">
<b>Логин:</b> {{username}}
<b>Authstr:</b> {{auth}}<br>
<b>Адрес:</b> {{nodename}}, {{addr}}<br>
<b>Режим чтения:
%if feed == 1:
<a href="/s/feed/0">Лента</a>
%else:
<a href="/s/feed/1">Почта</a>
%end
<br><br>
<a class="form-button" href="/logout">Выйти</a><br><br>
</div>
</div>
%include tpl/footer.tpl