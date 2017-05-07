%import api
%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
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

<div id="echolist">
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
</div>

%include tpl/footer.tpl