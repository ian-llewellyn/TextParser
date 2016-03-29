import unittest, tp

fields = 'USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n'
data   = 'root         1  0.0  0.1  46748  3168 ?        Ss   Mar25   0:06 /usr/lib/systemd/systemd --system --deserialize 14\n'

class LearningTest(unittest.TestCase):

    def testMultiSpace(self):
        parser = tp.TextParser()
        parser.learn(fields)
        self.assertEqual(['user', 'pid', 'cpu', 'mem',
                          'vsz', 'rss', 'tty', 'stat',
                          'start', 'time', 'command'],
                         parser.fields())

    def testTabSeps(self):
        parser = tp.TextParser()
        tab_fields = fields
        last_size = 0
        new_size = len(tab_fields)
        while last_size != new_size:
            last_size = new_size
            tab_fields = tab_fields.replace('  ', ' ')
            new_size = len(tab_fields)
        tab_fields = tab_fields.replace(' ', '\t')
        parser.learn(tab_fields)
        self.assertEqual(['user', 'pid', 'cpu', 'mem',
                          'vsz', 'rss', 'tty', 'stat',
                          'start', 'time', 'command'],
                         parser.fields())

    def testCommaSeps(self):
        parser = tp.TextParser()
        tab_fields = fields
        last_size = 0
        new_size = len(tab_fields)
        while last_size != new_size:
            last_size = new_size
            tab_fields = tab_fields.replace('  ', ' ')
            new_size = len(tab_fields)
        tab_fields = tab_fields.replace(' ', ',')
        parser.learn(tab_fields)
        self.assertEqual(['user', 'pid', 'cpu', 'mem',
                          'vsz', 'rss', 'tty', 'stat',
                          'start', 'time', 'command'],
                         parser.fields())

class InputTest(unittest.TestCase):

    def testDataMatchUp(self):
        parser = tp.TextParser()
        parser.learn(fields)
        self.assertEqual(parser.parse(data),
            {'user': 'root',
             'pid': 1,
             'cpu': 0.0,
             'mem': 0.1,
             'vsz': 46748,
             'rss': 3168,
             'tty': '?',
             'stat': 'Ss',
             'start': 'Mar25',
             'time': '0:06',
             'command': '/usr/lib/systemd/systemd --system --deserialize 14'})

    def testInputFormat(self):
        """127.0.0.1 - - [05/Sep/2015:23:26:01 +0100] "GET /TimeStripe.js/sample.html HTTP/1.1" 200 1224 "-" "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
127.0.0.1 - - [05/Sep/2015:23:26:01 +0100] "GET /TimeStripe.js/timestripe.css HTTP/1.1" 200 222 "http://127.0.0.1/TimeStripe.js/sample.html" "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
127.0.0.1 - - [05/Sep/2015:23:26:01 +0100] "GET /TimeStripe.js/timestripe.js HTTP/1.1" 200 2817 "http://127.0.0.1/TimeStripe.js/sample.html" "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
127.0.0.1 - - [05/Sep/2015:23:26:01 +0100] "GET /favicon.ico HTTP/1.1" 404 209 "http://127.0.0.1/TimeStripe.js/sample.html" "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
"""
        data = '127.0.0.1 - - [05/Sep/2015:23:26:01 +0100] "GET /TimeStripe.js/timestripe.js HTTP/1.1" 200 2817 "http://127.0.0.1/TimeStripe.js/sample.html" "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"\n'
        parser = tp.TextParser()
        parser.ip_format('%{ip} - - [%{datetime}] "%{request}" %{status} %{bytes} "%{referrer}" "%{useragent}"')
        self.assertEqual(parser.parse(data), {
            'ip': '127.0.0.1',
            'datetime': '05/Sep/2015:23:26:01 +0100',
            'request': 'GET /TimeStripe.js/timestripe.js HTTP/1.1',
            'status': 200,
            'bytes': 2817,
            'referrer': 'http://127.0.0.1/TimeStripe.js/sample.html',
            'useragent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'})

class OutputTest(unittest.TestCase):

    def testTest(self):
        self.assertEqual({'a': 5, 'b': 6}, {'b': 6, 'a': 5})

    def testFormatter(self):
        parser = tp.TextParser()
        parser.learn(fields)
        parser.op_format('%{pid} %{user} %{time} Some other text')
        self.assertEqual(parser.sprintf(data), '1 root 0:06 Some other text')
