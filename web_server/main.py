# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
import urllib
import json
import re

__author__ = 'oks'


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        import random
        colors = [u'192430', u'E29611', u'0A926A', u'2F75BE', u'CC2979']
        i = random.randrange(5)
        exp_path = re.compile(r'/exp[?].?(w+)?')
        if self.path == u'/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("""
            <form method=POST style="display: flex; align-items: center; justify-content: center; margin-bottom: 80px;
                  margin-top: 220px; ">
                <input name="n" type=text style="padding-left: 5px; width: 80%; height: 40px; border-color: #ddd; font-size: 16px;" />
                <input style="width: 60px; height: 40px; background-color: #{color}; font-family: Sans-Serif;
                    font-size: 22px; color: #fff; border: 0" type=submit value="Go!.." />
            </form>
            """.format(color=colors[i]))

        if re.match(exp_path, self.path):
            import urlparse
            from urllib import quote
            q = self.path.replace(u'/exp?q', u'q')
            query = urlparse.parse_qs(q).get(u'q')
            print query
            url = 'https://ajax.googleapis.com/ajax/services/feed/find?v=1.0&q=%s&userip=USERS-IP-ADDRESS&googlehost=google.ru' % quote(query[0].encode('utf-8'))
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            d = {}
            # yandex = dict(
            #     ya_url=u'',
            #     ya_title=u'',
            #     ya_content=u'',
            # )
            # d.update(yandex)
            print results
            data = results['responseData']
            # print 'Total results: %s' % data['entries']['estimatedResultCount']
            hits = data['entries']
            print 'Top %d hits:' % len(hits)
            google = dict(
                google_url=hits[0]['url'].encode('utf-8'),
                google_title=hits[0]['title'].encode('utf-8'),
                google_content=hits[0]['contentSnippet'].encode('utf-8'),
            )
            d.update(google)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("""
            <link href='http://fonts.googleapis.com/css?family=Roboto+Slab:400,700' rel='stylesheet' type='text/css'>
            <link href='http://fonts.googleapis.com/css?family=Roboto:500' rel='stylesheet' type='text/css'>
            <form method=POST style="display: flex; flex-direction: row; align-items: flex-start; ">

                <div style="display: flex; width: 45%; margin-left: 2%; flex-direction: column; align-items: flex-start; ">
                    <span style="color: #ffdd67; margin-bottom: 60px; font-size: 100px; align-self: center; font-family: Roboto; ">Yandex</span>
                    <a href={google_url} style="color: #192430; font-size: 30px; font-family: Roboto Slab">{google_title}</a>
                    <span style="font-family: Roboto; font-size: 16px; ">{google_content}</span>
                    <input name="n" style="font-size: 32px; margin-top: 60px; width: 60px; height: 60px; align-self: center; border-radius: 50%; border: 0; background-color: #ccc; color: #fff; padding-top: 4px; " type=submit value="&#9829" />
                </div>

                <div style="display: flex; width: 45%; margin-left: 6%; flex-direction: column; align-items: flex-start; ">
                    <span style="color: #9fd8f6; margin-bottom: 60px; font-size: 100px; align-self: center; font-family: Roboto; ">Google</span>
                    <a href={google_url} style="color: #192430; font-size: 30px; font-family: Roboto Slab">{google_title}</a>
                    <span style="font-family: Roboto; font-size: 16px; ">{google_content}</span>
                    <input name="n" style="font-size: 32px; margin-top: 60px; width: 60px; height: 60px; align-self: center; border-radius: 50%; border: 0; background-color: #ccc; color: #fff; padding-top: 4px; " type=submit value="&#9829" />
                </div>
            </form>
            """.format(**d))
        return

    def do_POST(self):
        from urllib import quote

        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD': 'POST',
                                         'CONTENT-TYPE': self.headers['Content-type']}
                                )

        query = form.getvalue('n')
        # query = urllib.urlencode({u'query': query})
        # if query not in [u'GOOGLE', u'YANDEX']:
            # url = 'http://yandex.ru/yandsearch?text=%s' % query
            # with open('path/to/file.xml') as fd:
            #     obj = xmltodict.parse(fd.read())
            # search_response = urllib.urlopen(url)
            # search_results = search_response.read()
            # results = json.loads(search_results)
            # print results
        self.send_response(301)
        self.send_header('Location', '/exp?q=%s' % quote(query.decode(encoding='utf-8').encode('utf-8')))
        self.end_headers()
        return

#   /experiment=121


server = HTTPServer(('', 8080), MyHandler)
if __name__ == u'__main__':
    try:
        server.serve_forever()
    except:
        server.socket.close()