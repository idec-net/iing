%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<script>
function clearSelect() {
document.getElementById("fileecho").options[0].selected = true;
}
function clearFecho() {
document.getElementById("fechoname").value = "";
}
</script>

<div id="bottom-buttons">
<a href="/" title="Главная"><i class="fa fa-home fa-2x bbutton"></i></a>
<i class="fa fa-arrow-circle-up fa-2x bbutton" onclick="document.body.scrollTop = document.documentElement.scrollTop = 0;" title="Наверх"></i>
</div>

<div id="panel">
<div id="buttons">
<a href="/s/filelist" class="button"><i class="fa fa-arrow-left"></i><span class="caption"> Назад</span></a>
</div>
<h3>Загрузка файла</h3>
</div><br>

<div id="conferences" class="width90 files">
<div align="left">
<form method="post" enctype="multipart/form-data" action="/a/savefile">
<div id="fecho">
Выберите файлэхоконференцию из списка или введите её название в поле ввода.<br>
<select id="fileecho" name="fileecho" onclick="clearFecho()">
<option selected></option>
%for fecho in fechoareas:
<option>{{fecho[0]}}</option>
%end
</select>
<input type="text" name="tfileecho" id="fechoname" onclick="clearSelect()"><br><br>
</div>
<input type="file" name="file"><br><br>
<input type="text" name="dsc" placeholder="Описание"><br><br>
<input class="form-button" type="submit" value="Загрузить">
</form>
</div>
</div>

%include tpl/footer.tpl
