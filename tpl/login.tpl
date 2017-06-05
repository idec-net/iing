%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
<h3>Авторизация</h3>
</div><br>

<div id="conferences" class="width90">
<h3>Введите имя пользователя и пароль</h3>
%if alarm:
<span class="alarm">{{alarm}}</span>
%end
<form method="post" enctype="multipart/form-data" action="/login">
%if username:
<input type="text" name="username" class="input input_line login" placeholder="username" value={{username}}><br>
%else:
<input type="text" name="username" class="input input_line login" placeholder="username"><br>
%end
%if auth:
<input type="password" name="password" class="input input_line login" placeholder="password" value={{auth}}><br>
%else:
<input type="password" name="password" class="input input_line login" placeholder="password"><br>
%end
<button class="form-button">Отправить</button>
</form>
</div>
%include tpl/footer.tpl