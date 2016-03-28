#!/bin/python
# -*- coding: utf-8 -*-

def iswhitespace(c):
    if c == ' ' or c == '\t':
        return True
    return False

class TextParser(object):
    def __init__(self):
        self.field_list = []

    def fields(self):
        return self.field_list

    def learn(self, subject):
        subject = subject.rstrip('\n')
        self.construction = []
        field_title = ''
        for c in subject:
            if c.isalnum():
               field_title += c.lower()
               continue
            if c == ' ' or c == '\t' or c == ',':
                self.separator = c
                field_title != '' and self.field_list.append(field_title)
                field_title = ''
        field_title != '' and self.field_list.append(field_title.lower())
        #raise Exception('Unable to learn from this subject')

    def parse(self, data):
        data = data.rstrip('\n')
        result = {}
        for field in self.field_list:
            head, sep, tail = data.partition(self.separator)
            while head == '':
                data = tail
                head, sep, tail = data.partition(self.separator)
            result[field] = head
            data = tail
        result[field] += self.separator + tail

        for k in result.keys():
            try:
                result[k] = int(result[k])
                continue
            except ValueError:
                pass

            try:
                result[k] = float(result[k])
            except ValueError:
                pass

        return result

    def op_format(self, format_string):
        self.format_string = format_string

    def sprintf(self, data):
        output = ''
        parsed = self.parse(data)
        in_var = False
        var_name = ''
        last_c = None
        for c in self.format_string:
            if in_var and c == '}':
                output += str(parsed[var_name])
                in_var = False
                var_name = ''
                last_c = c
                continue
            if in_var:
                var_name += c
                last_c = c
                continue
            if not in_var and last_c == '%' and c == '{':
                in_var = True
                last_c = c
                continue
            if not in_var and last_c == '%' and c == '%':
                output += last_c + c
                last_c = c
                continue
            if not in_var and c == '%':
                last_c = c
                continue
            output += c
            last_c = c
        return output

class Field(object):
    def __init__(self, name, width=None, just=None):
        pass


class Separator(object):
    pass


class Line(object):
    pass
    #(
    #    Field,Separator,Field,Separator,Field
    #)

if __name__ == '__main__':
    import sys, os
    tp = TextParser()
    tp.learn(sys.stdin.readline())
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        line == '' and sys.exit(os.EX_OK)
        print tp.parse(sys.stdin.readline())
