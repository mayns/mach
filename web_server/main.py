# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
import urllib
import json
import re

__author__ = 'oks'


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self, **kwargs):

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
            margin-top: 80px; ">
                <span style="font-size: 30px; margin-right: 20px; line-height: 30px; "><strong>~#: </strong></span>
                <input name="n" type=text style="width: 80%; height: 30px; font-size: 14px;" />
                <input style="width: 50px; height: 30px; background-color: #{color}; font-family: Sans-Serif;
                    font-size: 18px; color: #fff; border: 0" type=submit value="Go!.." />
            </form>
            """.format(color=colors[i]))

        if re.match(exp_path, self.path):
            import urlparse
            q = self.path.replace(u'/exp?q', u'q')
            query = urlparse.parse_qs(q).get(u'q')
            m = {}
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=large' % query
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            print results
            data = results['responseData']
            print 'Total results: %s' % data['cursor']['estimatedResultCount']
            hits = data['results']
            print 'Top %d hits:' % len(hits)
            for h in hits: print m.update(h)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("""
            <form method=POST style="display: flex; width: 100%; justify-content: space-around;">
                <div style="text-align: center; ">YANDEX</div>
                <input name="n" style="width: 420px; height:120px; background-color: #2F75BE; font-family: Sans-Serif;
                    font-size: 90px; color: #fff; border: 0" type=submit value="YANDEX" />

                <div style="text-align: center; ">GOOGLE</div>
                <div>{data}</div>
                <input name="n" style="width: 420px; height:120px; background-color: #2F75BE; font-family: Sans-Serif;
                    font-size: 90px; color: #fff; border: 0" type=submit value="GOOGLE" />
            </form>
            """.format(data=m))
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
        self.send_header('Location', '/exp?q=%s' % quote(query).encode('utf-8'))
        self.end_headers()
        return

#   /experiment=121


server = HTTPServer(('', 8080), MyHandler)
if __name__ == u'__main__':
    try:
        server.serve_forever()
    except:
        server.socket.close()