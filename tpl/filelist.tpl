%import os
%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="bottom-buttons">
<a href="/" title="Главная"><i class="fa fa-home fa-2x bbutton"></i></a>
<i class="fa fa-arrow-circle-up fa-2x bbutton" onclick="document.body.scrollTop = document.documentElement.scrollTop = 0;" title="Наверх"></i>
</div>

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
%if auth:
<div id="rbuttons">
<a href="/s/upload" class="button"><i class="fa fa-upload"></i><span class="caption"> Загрузить</span></a>
</div>
%end
<h3>Список файлов</h3>
</div><br>

<div id="conferences" class="width90 files">
<table border="0" cellpadding="0" cellspacing="0" id="filelist">
%if d:
<tr><td><a href="/s/filelist">../</a></td><td></td><td></td></tr>
%end
%for file in files:
<tr>
<td>
%if file[0].endswith("/"):
<a href="/s/filelist/{{file[0].replace("/", "")}}">{{file[0]}}</a>
%else:
<a href="/s/download/{{file[1]}}/{{file[0]}}">{{file[0]}}</a>
%end
</td>
<td>
%if file[2]:
%size = int(file[2])
%if size < 1024:
%    size = str(size) + " B"
%else:
%    size = str(int(size / 1024 * 10) / 10) + " KB"
%end
{{size}}
</td>
%end
<td>
{{file[3]}}
</td>
</tr>
%end
</table>
</div>

<div id="conferences" class="mfiles">
<table border="0" cellpadding="0" cellspacing="0" id="filelist">
%if d:
<tr><td><a href="/s/filelist">../</a></td><td></td></tr>
%end
%for file in files:
<tr>
<td>
%if file[0].endswith("/"):
<a href="/s/filelist/{{file[0].replace("/", "")}}">{{file[0]}}</a>
%else:
<a href="/s/download/{{file[1]}}/{{file[0]}}">{{file[0]}}</a><br>
{{file[3]}}
%end
</td>
<td>
%if file[2]:
%size = int(file[2])
%if size < 1024:
%    size = str(size) + " B"
%else:
%    size = str(int(size / 1024 * 10) / 10) + " KB"
%end
{{size}}
</td>
%end
</tr>
</a>
%end
</table>
</div>

<br><br>

%include tpl/footer.tpl