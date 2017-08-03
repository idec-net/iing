<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.1 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="/lib/css/font-awesome.min.css">
    <link rel="icon" href="/lib/idec.png" type="image/png">
    <link rel="stylesheet" type="text/css" href="/lib/css/style.css">
    <meta name="viewport" content="width=device-width; initial-scale=1.0">
    <title>{{nodename}}</title>
    <script>
      window.onscroll = function() {
      var top = document.body.scrollTop + document.documentElement.scrollTop == 0;
      document.getElementById('bottom-buttons').style.display = top ? 'none' : 'block';
      }
    </script>
  </head>
  %import random
  %image = random.choice(background)
  <body style="background: url(/lib/{{image}}) no-repeat; background-size: cover; -webkit-background-size: cover; background-attachment: fixed;">
    <center>
