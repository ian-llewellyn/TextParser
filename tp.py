#!/bin/python
# -*- coding: utf-8 -*-

def iswhitespace(c):
    if c == ' ' or c == '\t':
        return True
    return False

class TextParser(object):
    def __init__(self):
        self.record_construction = []

    def fields(self):
        result = []
        for component in self.record_construction:
            isinstance(component, Field) and result.append(component.name)
        return result

    def learn(self, subject):
        subject = subject.rstrip('\n')
        field_title = ''
        for c in subject:
            if c.isalnum():
               field_title += c.lower()
               continue
            if c == ' ' or c == '\t' or c == ',':
                if field_title == '':
                    self.record_construction[len(self.record_construction)-1].variable = True
                    continue
                self.record_construction.append(Field(field_title))
                c == ' ' and self.record_construction.append(Separator(c, variable=True))
                c != ' ' and self.record_construction.append(Separator(c))
                field_title = ''
        if field_title != '':
            self.record_construction.append(Field(field_title))
        #raise Exception('Unable to learn from this subject')

    def parse(self, data):
        # strict = input format provided
        # relaxed = input fields learned
        # csv | csv with commas in double quotes
        # single space | multiple spaces
        # raw = include padding
        data = data.rstrip('\n')

        result = {}
        record_construction = list(self.record_construction)
        while True:
            try:
                component = record_construction.pop(0)
            except IndexError:
                # We have reached the end of the expectations
                break

            if isinstance(component, Separator):
                # search for separator in data - should this always be 0
                # chew it out of data
                if component.variable == True:
                    while data.find(component.chars) == 0:
                        data = data[sep_pos + len(next_sep):]
                else:
                    data = data[sep_pos + len(next_sep):]
                # move on
                continue

            if isinstance(component, Field):
                try:
                    # search for the next expected separator
                    next_sep = record_construction.pop(0)
                    # One Field followed by another would be weird!
                    assert(isinstance(next_sep, Separator))
                    # ...and find it in the haystack
                    next_sep_pos = data.find(next_sep.chars)
                except IndexError:
                    # no other separators, take the rest of the record
                    result[component.name] = data
                    data = ''
                else:
                    # take everything beetween here and there as the field data
                    result[component.name] = data[:next_sep_pos]
                    data = data[next_sep_pos + len(next_sep):]
                    if next_sep.variable == True:
                        while data.find(next_sep.chars) == 0:
                            data = data[len(next_sep):]

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
        self.op_format_string = format_string

    def sprintf(self, data):
        output = ''
        parsed = self.parse(data)
        in_var = False
        var_name = ''
        last_c = None
        for c in self.op_format_string:
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

    def ip_format(self, format_string):
        self.ip_format_string = format_string
        sep_chars = ''
        in_var = False
        var_name = ''
        last_c = None
        for c in self.ip_format_string:
            if in_var and c == '}':
                self.record_construction.append(Field(var_name))
                in_var = False
                var_name = ''
                last_c = c
                continue
            if in_var:
                var_name += c
                last_c = c
                continue
            if not in_var and last_c == '%' and c == '{':
                sep_chars != '' and self.record_construction.append(Separator(sep_chars))
                sep_chars = ''
                in_var = True
                last_c = c
                continue
            if not in_var and last_c == '%' and c == '%':
                sep_chars += last_c + c
                last_c = c
                continue
            if not in_var and c == '%':
                last_c = c
                continue
            sep_chars += c
            last_c = c
        if sep_chars != '':
            self.record_construction.append(Separator(sep_chars))

class Field(object):
    def __init__(self, name, width=None, just=None):
        self.name = name
        self.width = width
        self.just = just

    def __len__(self):
        return len(self.width) or len(self.name)

    def __repr__(self):
        return 'Field: %s' % self.name

class Separator(object):
    def __init__(self, chars, variable=False):
        self.chars = chars
        self.variable = variable

    def __len__(self):
        return len(self.chars)

    def __repr__(self):
        return "Separator: '%s'" % self.chars

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
        print tp.parse(line)
