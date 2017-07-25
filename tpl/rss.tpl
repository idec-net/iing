%import api
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
 <channel>
  <title>{{nodename}}</title>
  <description>{{dsc}}: {{echoarea}}</description>
  <link>{{nodeurl}}</link>
  <language>ru</language>
%for msg in msgs:
<item>
<name>{{msg[1][6]}}</name>
<title>{{msg[1][6]}}</title>
%body = "<b>%s</b> to <b>%s</b><br><br>%s" % (msg[1][3], msg[1][5], "<br>".join(msg[1][8:]))
<description>{{body}}</description>
%time = api.rss_time(msg[1][2])
<pubDate>{{time}}</pubDate>
<author>{{msg[1][3]}}</author>
<link>{{nodeurl}}{{msg[0]}}</link>
<guid>{{msg[0]}}</guid>
</item>
%end
</channel>
</rss>