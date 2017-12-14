%include tpl/header.tpl nodename=nodename, dsc=dsc, background=background

<div id="panel">
<div id="buttons">
<a href="/" class="button"><i class="fa fa-home"></i><span class="caption"> Главная</span></a>
</div>
</div><br>

<div id="conferences" class="width90 files">
<h2>{{message}}</h2>
<a class="form-button" href="/s/filelist">К списку файлов</a><br><br>
</div>

%include tpl/footer.tpl