%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
<h3>Профиль</h3>
</div><br>

<div id="conferences" class="width90">
<div align="left">
<b>Логин:</b> {{username}}<br>
<b>Authstr:</b> {{auth}}<br>
<b>Адрес:</b> {{nodename}}, {{addr}}<br><br>
<a class="form-button" href="/logout">Выйти</a><br><br>
</div>
</div>
%include tpl/footer.tpl