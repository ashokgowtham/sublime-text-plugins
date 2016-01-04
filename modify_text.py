import sublime
import sublime_plugin
import re
import os
import random
from operator import itemgetter
from .edit import *

random.seed(1)

obj = {'levelStack': [0], 'valueStack': [''], 'delimiter': '.'}
autoDetectIndentPattern = False


class ConvertCaseCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                text = increment(self.view.substr(region))
                print(text)
                self.view.replace(edit, region, text)


class FlattenYamlCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        entire_text_region = sublime.Region(0, self.view.size())
        text = flatten_yaml_text(self.view.substr(entire_text_region))
        self.view.replace(edit, entire_text_region, text)


class PadRightCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selections = []   # (text, region, start_col, end_col)

        for region in self.view.sel():
            selections.append((self.view.substr(region),
                               region,
                               self.view.rowcol(region.a)[1],
                               self.view.rowcol(region.b)[1]))
        max_end_col = max([end_col for (_, _, _, end_col) in selections])
        padding = [' ' * (max_end_col - end_col)
                   for (text, region, _, end_col) in selections]
        padding.reverse()
        print(padding)
        for region in self.view.sel():
            p = padding.pop()
            print((p))
            self.view.replace(edit, region, self.view.substr(region) + p)


class IntersectSelectionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        index = -1
        for region in self.view.sel():
            index = index + 1
            if region.empty():
                self.view.replace(edit, self.view.sel()[0], "")
            text = self.view.substr(region)
            cur_lines = text.split('\n')
            if index == 0:
                intersected_lines = cur_lines
                continue
            lines = intersected_lines
            for line in intersected_lines:
                if line not in cur_lines:
                    lines.remove(line)
            intersected_lines = lines
        index = -1
        for region in self.view.sel():
            index = index + 1
            if index == 0:
                self.view.replace(edit, region, '\n'.join(lines))
            else:
                self.view.replace(edit, region, '')


# sort and then run this command
# runs on entire file
class GroupByAndCountCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        entire_text_region = sublime.Region(0, self.view.size())
        text = group_by_count_text(self.view.substr(entire_text_region))
        self.view.replace(edit, entire_text_region, text)


def group_by_count_text(text):
    d = {}
    lines = text.split(os.linesep)
    for line in lines:
        d[line] = (d.get(line) or 0) + 1
    return os.linesep.join(
        '%s %s' % (v, k) for (k, v) in
        sorted(d.items(), key=itemgetter(1), reverse=True))


def indentLevel(text):
    if (obj.get('indent') is None):
        m = re.match("^[ \t]+", text)
        if (m):
            obj['indent'] = text[m.start():m.end()]
            return 1
        else:
            return 0
    level = 0
    if autoDetectIndentPattern:
        p = obj['indent']
    else:
        p = ' '
    m = re.match(p, text)
    while(m):
        text = text[m.end():]
        level = level + 1
        m = re.match(p, text)
    return level


def getLevel():
    return obj['levelStack'][-1]


def flatten_yaml_text(text):
    lines = text.split('\n')
    flattened = []
    for line in lines:
        value = line.strip()
        if(value == ""):
            flattened.append('\n')
            continue
        if(value[0] == "#"):
            flattened.append('\n')
            continue
        level = indentLevel(line)
        while(getLevel() > level):
            obj['levelStack'].pop()
            obj['valueStack'].pop()
        if(level > getLevel()):
            obj['levelStack'].append(level)
        else:
            obj['valueStack'].pop()
        value = re.sub(':[ ]*$', '', value)
        obj['valueStack'].append(value.strip())

        flattened.append(obj.get('delimiter').join(obj['valueStack']) + "\n")
    return ''.join(flattened)[0:-1]


def isCharacter(c):
    return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z'


def isUpper(c):
    return c >= 'A' and c <= 'Z'


def isLower(c):
    return c >= 'A' and c <= 'Z'


def isPunctuation(c):
    return not (isNumeric(c) or isCharacter(c))


def get_components(word):
    methods = [isCharacter, isUpper, isLower, isNumeric]
    data = map(lambda x: map(lambda y: y(x), methods), word)

    for d, i in data:
        pass
