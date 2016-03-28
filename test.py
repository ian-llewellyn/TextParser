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

class DataTest(unittest.TestCase):

    def testMatchUp(self):
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

class OutputTest(unittest.TestCase):

    def testTest(self):
        self.assertEqual({'a': 5, 'b': 6}, {'b': 6, 'a': 5})

    def testFormatter(self):
        parser = tp.TextParser()
        parser.learn(fields)
        parser.op_format('%{pid} %{user} %{time} Some other text')
        #parser.op_format('%(pid)d %(user)s %(time)s Some other text')
        self.assertEqual(parser.sprintf(data), '1 root 0:06 Some other text')
