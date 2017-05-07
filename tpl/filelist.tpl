%import os
%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
<h3>Список файлов</h3>
</div><br>

<div id="conferences" class="width90">
ВНИМАНИЕ! Не передавайте никому ссылки с этой страницы. В них может содержаться ваш authkey.<br>
<table border="0" cellpadding="0" cellspacing="0" id="filelist">
%for file in files:
<tr>
<td>
%if auth:
<a href="/x/file/{{auth}}/{{file[0]}}">{{file[0]}}</a>
%else:
<a href="/x/file/{{file[0]}}">{{file[0]}}</a>
%end
</td>
<td>
%size = int(file[1])
%if size < 1024:
%    size = str(size) + " B"
%else:
%    size = str(int(size / 1024 * 10) / 10) + " KB"
%end
{{size}}
</td>
<td>
{{file[2]}}
</td>
</tr>
%end
</table>
</div>
%include tpl/footer.tpl